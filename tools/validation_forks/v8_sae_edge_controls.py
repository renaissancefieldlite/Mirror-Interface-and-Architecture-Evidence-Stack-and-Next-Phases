#!/usr/bin/env python3
"""SAE feature-to-feature edge controls for the V8 circuit layer.

This runner tests the exported SAE edge graph as its own artifact. The first
SAE pilot already supported feature-level context separation; this gate asks
whether the exported feature-to-feature edge rows carry context structure above
label-shuffle controls and above a hub / degree-style baseline.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
EDGE_PATH = (
    ROOT
    / "artifacts"
    / "validation"
    / "v8_sae_feature_circuit_exports"
    / "v8_sae_feature_circuit_edges.csv"
)
OUT_DIR = ROOT / "artifacts" / "validation" / "v8_sae_edge_controls"
SEED = 67
SHUFFLES = 200


def load_edges() -> pd.DataFrame:
    if not EDGE_PATH.exists():
        raise FileNotFoundError(f"Missing SAE edge export: {EDGE_PATH}")
    edges = pd.read_csv(EDGE_PATH)
    required = {
        "model",
        "prompt_set",
        "context",
        "token_region",
        "source_layer",
        "source_feature_id",
        "target_layer",
        "target_feature_id",
        "edge_weight",
        "edge_type",
    }
    missing = sorted(required - set(edges.columns))
    if missing:
        raise ValueError(f"SAE edge export missing columns: {missing}")
    edges = edges.copy()
    edges["source_layer"] = edges["source_layer"].astype(int)
    edges["target_layer"] = edges["target_layer"].astype(int)
    edges["source_feature_id"] = edges["source_feature_id"].astype(int)
    edges["target_feature_id"] = edges["target_feature_id"].astype(int)
    edges["edge_weight"] = edges["edge_weight"].astype(float)
    edges["layer_gap"] = edges["target_layer"] - edges["source_layer"]
    edges["same_feature"] = (edges["source_feature_id"] == edges["target_feature_id"]).astype(int)
    edges["feature_pair"] = (
        edges["source_feature_id"].astype(str) + "->" + edges["target_feature_id"].astype(str)
    )
    edges["layer_pair"] = edges["source_layer"].astype(str) + "->" + edges["target_layer"].astype(str)
    return edges


def add_degree_features(edges: pd.DataFrame) -> pd.DataFrame:
    enriched = edges.copy()
    source_counts = enriched["source_feature_id"].value_counts()
    target_counts = enriched["target_feature_id"].value_counts()
    pair_counts = enriched["feature_pair"].value_counts()
    layer_pair_counts = enriched["layer_pair"].value_counts()
    enriched["source_feature_degree"] = enriched["source_feature_id"].map(source_counts).astype(float)
    enriched["target_feature_degree"] = enriched["target_feature_id"].map(target_counts).astype(float)
    enriched["feature_pair_degree"] = enriched["feature_pair"].map(pair_counts).astype(float)
    enriched["layer_pair_degree"] = enriched["layer_pair"].map(layer_pair_counts).astype(float)
    enriched["log_edge_weight"] = np.log1p(np.maximum(enriched["edge_weight"].to_numpy(), 0.0))
    return enriched


def matrix(edges: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode == "full_edge":
        base = edges[
            [
                "edge_weight",
                "log_edge_weight",
                "source_layer",
                "target_layer",
                "layer_gap",
                "same_feature",
                "source_feature_id",
                "target_feature_id",
                "source_feature_degree",
                "target_feature_degree",
                "feature_pair_degree",
                "layer_pair_degree",
                "model",
                "token_region",
                "source_feature_id",
                "target_feature_id",
                "feature_pair",
                "layer_pair",
            ]
        ].copy()
        return pd.get_dummies(
            base,
            columns=["model", "token_region", "source_feature_id", "target_feature_id", "feature_pair", "layer_pair"],
            dtype=float,
        )
    if mode == "degree_baseline":
        base = edges[
            [
                "edge_weight",
                "log_edge_weight",
                "source_layer",
                "target_layer",
                "layer_gap",
                "same_feature",
                "source_feature_degree",
                "target_feature_degree",
                "feature_pair_degree",
                "layer_pair_degree",
                "model",
                "token_region",
                "layer_pair",
            ]
        ].copy()
        return pd.get_dummies(base, columns=["model", "token_region", "layer_pair"], dtype=float)
    if mode == "hub_only":
        return edges[
            [
                "edge_weight",
                "log_edge_weight",
                "source_feature_degree",
                "target_feature_degree",
                "feature_pair_degree",
                "layer_pair_degree",
            ]
        ].copy()
    raise ValueError(f"Unknown feature mode: {mode}")


def score_matrix(x: pd.DataFrame, y: np.ndarray, shuffle_count: int = SHUFFLES) -> dict[str, Any]:
    train_x, test_x, train_y, test_y = train_test_split(
        x.to_numpy(dtype=float),
        y,
        test_size=0.30,
        random_state=SEED,
        stratify=y,
    )
    clf = make_pipeline(
        StandardScaler(with_mean=False),
        LogisticRegression(max_iter=1000, random_state=SEED),
    )
    clf.fit(train_x, train_y)
    observed = float(balanced_accuracy_score(test_y, clf.predict(test_x)))

    rng = np.random.default_rng(SEED)
    shuffled_scores = []
    for _ in range(shuffle_count):
        shuffled_y = rng.permutation(train_y)
        control = make_pipeline(
            StandardScaler(with_mean=False),
            LogisticRegression(max_iter=1000, random_state=SEED),
        )
        control.fit(train_x, shuffled_y)
        shuffled_scores.append(float(balanced_accuracy_score(test_y, control.predict(test_x))))
    shuffled = np.asarray(shuffled_scores)
    return {
        "observed_balanced_accuracy": observed,
        "shuffled_balanced_accuracy_mean": float(shuffled.mean()),
        "shuffled_balanced_accuracy_p95": float(np.percentile(shuffled, 95)),
        "shuffle_count": shuffle_count,
        "shuffle_p_value": float((np.sum(shuffled >= observed) + 1) / (shuffle_count + 1)),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 SAE Edge Controls",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Inputs",
        "",
        f"- edge rows: `{report['inputs']['edge_rows']}`",
        f"- context counts: `{report['inputs']['context_counts']}`",
        f"- model counts: `{report['inputs']['model_counts']}`",
        f"- token-region counts: `{report['inputs']['token_region_counts']}`",
        "",
        "## Edge-Control Scores",
        "",
        "| Feature set | Observed balanced accuracy | Shuffle mean | Shuffle p95 | p-value |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, result in report["scores"].items():
        lines.append(
            f"| `{name}` | `{result['observed_balanced_accuracy']:.6f}` | "
            f"`{result['shuffled_balanced_accuracy_mean']:.6f}` | "
            f"`{result['shuffled_balanced_accuracy_p95']:.6f}` | "
            f"`{result['shuffle_p_value']:.6f}` |"
        )
    lines.extend(["", "## Baseline Comparison", ""])
    for key, value in report["baseline_comparison"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Next Gates", ""])
    for item in report["next_gates"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    edges = add_degree_features(load_edges())
    y = edges["context"].to_numpy()
    scores = {
        "full_edge": score_matrix(matrix(edges, "full_edge"), y),
        "degree_baseline": score_matrix(matrix(edges, "degree_baseline"), y),
        "hub_only": score_matrix(matrix(edges, "hub_only"), y),
    }
    full = scores["full_edge"]["observed_balanced_accuracy"]
    degree = scores["degree_baseline"]["observed_balanced_accuracy"]
    hub = scores["hub_only"]["observed_balanced_accuracy"]
    p_value = scores["full_edge"]["shuffle_p_value"]
    supported = full > scores["full_edge"]["shuffled_balanced_accuracy_p95"] and p_value <= 0.05
    beats_degree = full > degree
    beats_hub = full > hub
    status = (
        "sae_edge_controls_supported"
        if supported and beats_degree and beats_hub
        else "sae_edge_controls_supported_label_shuffle_degree_open"
        if supported
        else "sae_edge_controls_open"
    )
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "clean_read": (
            "The exported SAE feature-to-feature edge graph carries context structure above shuffled-label controls "
            "and beats the degree / hub baselines. This supports the edge-specific circuit layer as the next "
            "interpretability rung."
            if status == "sae_edge_controls_supported"
            else "The exported SAE feature-to-feature edge graph carries context structure above shuffled-label controls, "
            "while degree / hub baselines remain competitive. The feature layer stays supported and the edge layer needs "
            "stronger edge-specific controls before closeout."
            if status == "sae_edge_controls_supported_label_shuffle_degree_open"
            else "The exported SAE feature-to-feature edge graph did not separate above shuffled-label controls under this gate. "
            "The feature layer remains supported; edge-specific circuit support stays open."
        ),
        "inputs": {
            "edge_rows": int(len(edges)),
            "context_counts": dict(Counter(edges["context"].tolist())),
            "model_counts": dict(Counter(edges["model"].tolist())),
            "token_region_counts": dict(Counter(edges["token_region"].tolist())),
        },
        "scores": scores,
        "baseline_comparison": {
            "full_minus_degree": round(float(full - degree), 6),
            "full_minus_hub": round(float(full - hub), 6),
            "beats_degree_baseline": bool(beats_degree),
            "beats_hub_baseline": bool(beats_hub),
        },
        "next_gates": [
            "export matching SAE activations for rerun_02 and prompt_set_02 when dense hidden-vector inputs exist",
            "run feature-frequency and token-window shuffled controls over the exported edge graph",
            "run optional feature / circuit ablations on top edge paths",
        ],
    }
    json_path = OUT_DIR / "v8_sae_edge_controls_report.json"
    md_path = OUT_DIR / "v8_sae_edge_controls_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path), "scores": scores}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
