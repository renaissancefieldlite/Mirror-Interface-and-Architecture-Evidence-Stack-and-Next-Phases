#!/usr/bin/env python3
"""SAE feature and edge ablation controls.

This runner uses the real bounded SAE pilot exports. It asks whether removing
the strongest exported architecture-carrying SAE features reduces context
separation more than matched random feature removals.
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
EXPORT_DIR = ROOT / "artifacts" / "validation" / "v8_sae_feature_circuit_exports"
ACTIVATIONS = EXPORT_DIR / "v8_sae_feature_activations.csv"
DICTIONARY = EXPORT_DIR / "v8_sae_feature_dictionary.csv"
EDGES = EXPORT_DIR / "v8_sae_feature_circuit_edges.csv"
OUT_DIR = ROOT / "artifacts" / "validation" / "v8_sae_ablation_controls"
SEED = 67
ABLATE_N = 8
RANDOM_TRIALS = 100


def load_activation_matrix() -> tuple[pd.DataFrame, np.ndarray, dict[str, Any]]:
    activations = pd.read_csv(ACTIVATIONS)
    required = {"sample_id", "context", "feature_id", "activation", "model", "layer_depth", "token_region"}
    missing = required - set(activations.columns)
    if missing:
        raise ValueError(f"Activation export missing columns: {sorted(missing)}")
    matrix = activations.pivot_table(
        index="sample_id",
        columns="feature_id",
        values="activation",
        aggfunc="max",
        fill_value=0.0,
    )
    matrix = matrix.reindex(columns=range(int(activations["feature_id"].max()) + 1), fill_value=0.0)
    labels = (
        activations.sort_values("sample_id")
        .drop_duplicates("sample_id")
        .set_index("sample_id")
        .loc[matrix.index]
    )
    meta = {
        "sample_rows": int(matrix.shape[0]),
        "feature_count": int(matrix.shape[1]),
        "context_counts": dict(Counter(labels["context"].tolist())),
        "model_counts": dict(Counter(labels["model"].tolist())),
    }
    return matrix, labels["context"].to_numpy(), meta


def architecture_features(count: int = ABLATE_N) -> list[int]:
    dictionary = pd.read_csv(DICTIONARY)
    dictionary["abs_lattice_lift"] = dictionary["lattice_lift_vs_controls"].abs()
    return dictionary.sort_values("abs_lattice_lift", ascending=False)["feature_id"].head(count).astype(int).tolist()


def score_feature_matrix(x: pd.DataFrame, y: np.ndarray) -> float:
    train_x, test_x, train_y, test_y = train_test_split(
        x.to_numpy(dtype=float),
        y,
        test_size=0.30,
        random_state=SEED,
        stratify=y,
    )
    clf = make_pipeline(StandardScaler(with_mean=False), LogisticRegression(max_iter=1000, random_state=SEED))
    clf.fit(train_x, train_y)
    return float(balanced_accuracy_score(test_y, clf.predict(test_x)))


def feature_ablation() -> dict[str, Any]:
    matrix, y, meta = load_activation_matrix()
    top_features = architecture_features()
    full_score = score_feature_matrix(matrix, y)
    top_removed_score = score_feature_matrix(matrix.drop(columns=top_features, errors="ignore"), y)
    top_drop = full_score - top_removed_score

    rng = np.random.default_rng(SEED)
    all_features = list(matrix.columns.astype(int))
    random_drops = []
    for _ in range(RANDOM_TRIALS):
        remove = rng.choice(all_features, size=len(top_features), replace=False).tolist()
        score = score_feature_matrix(matrix.drop(columns=remove, errors="ignore"), y)
        random_drops.append(full_score - score)
    random_arr = np.asarray(random_drops)
    p_value = float((np.sum(random_arr >= top_drop) + 1) / (RANDOM_TRIALS + 1))
    return {
        "metadata": meta,
        "top_features": top_features,
        "full_balanced_accuracy": full_score,
        "top_removed_balanced_accuracy": top_removed_score,
        "top_feature_drop": top_drop,
        "random_drop_mean": float(random_arr.mean()),
        "random_drop_p95": float(np.percentile(random_arr, 95)),
        "random_trials": RANDOM_TRIALS,
        "drop_p_value": p_value,
        "feature_ablation_supported": bool(top_drop > np.percentile(random_arr, 95) and p_value <= 0.05),
    }


def prepare_edges(edges: pd.DataFrame) -> pd.DataFrame:
    prepared = edges.copy()
    prepared["source_layer"] = prepared["source_layer"].astype(int)
    prepared["target_layer"] = prepared["target_layer"].astype(int)
    prepared["source_feature_id"] = prepared["source_feature_id"].astype(int)
    prepared["target_feature_id"] = prepared["target_feature_id"].astype(int)
    prepared["edge_weight"] = prepared["edge_weight"].astype(float)
    prepared["layer_gap"] = prepared["target_layer"] - prepared["source_layer"]
    prepared["same_feature"] = (prepared["source_feature_id"] == prepared["target_feature_id"]).astype(int)
    prepared["feature_pair"] = (
        prepared["source_feature_id"].astype(str) + "->" + prepared["target_feature_id"].astype(str)
    )
    prepared["layer_pair"] = prepared["source_layer"].astype(str) + "->" + prepared["target_layer"].astype(str)
    prepared["log_edge_weight"] = np.log1p(np.maximum(prepared["edge_weight"].to_numpy(), 0.0))
    return prepared


def edge_matrix(edges: pd.DataFrame) -> pd.DataFrame:
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
            "model",
            "token_region",
            "feature_pair",
            "layer_pair",
        ]
    ].copy()
    return pd.get_dummies(
        base,
        columns=["model", "token_region", "source_feature_id", "target_feature_id", "feature_pair", "layer_pair"],
        dtype=float,
    )


def score_edges(edges: pd.DataFrame) -> float:
    if len(edges) < 100:
        return 0.0
    x = edge_matrix(edges)
    y = edges["context"].to_numpy()
    train_x, test_x, train_y, test_y = train_test_split(
        x.to_numpy(dtype=float),
        y,
        test_size=0.30,
        random_state=SEED,
        stratify=y,
    )
    clf = make_pipeline(StandardScaler(with_mean=False), LogisticRegression(max_iter=1000, random_state=SEED))
    clf.fit(train_x, train_y)
    return float(balanced_accuracy_score(test_y, clf.predict(test_x)))


def edge_ablation(top_features: list[int]) -> dict[str, Any]:
    edges = prepare_edges(pd.read_csv(EDGES))
    full_score = score_edges(edges)
    mask = ~edges["source_feature_id"].isin(top_features) & ~edges["target_feature_id"].isin(top_features)
    top_removed = edges[mask].copy()
    top_removed_score = score_edges(top_removed)
    top_drop = full_score - top_removed_score

    rng = np.random.default_rng(SEED)
    all_features = sorted(set(edges["source_feature_id"].tolist()) | set(edges["target_feature_id"].tolist()))
    random_drops = []
    random_rows_remaining = []
    for _ in range(RANDOM_TRIALS):
        remove = set(rng.choice(all_features, size=len(top_features), replace=False).tolist())
        kept = edges[~edges["source_feature_id"].isin(remove) & ~edges["target_feature_id"].isin(remove)].copy()
        random_rows_remaining.append(int(len(kept)))
        random_drops.append(full_score - score_edges(kept))
    random_arr = np.asarray(random_drops)
    p_value = float((np.sum(random_arr >= top_drop) + 1) / (RANDOM_TRIALS + 1))
    return {
        "edge_rows": int(len(edges)),
        "top_removed_edge_rows": int(len(top_removed)),
        "random_rows_remaining_mean": float(np.mean(random_rows_remaining)),
        "full_balanced_accuracy": full_score,
        "top_removed_balanced_accuracy": top_removed_score,
        "top_edge_feature_drop": top_drop,
        "random_drop_mean": float(random_arr.mean()),
        "random_drop_p95": float(np.percentile(random_arr, 95)),
        "random_trials": RANDOM_TRIALS,
        "drop_p_value": p_value,
        "edge_ablation_supported": bool(top_drop > np.percentile(random_arr, 95) and p_value <= 0.05),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    f = report["feature_ablation"]
    e = report["edge_ablation"]
    lines = [
        "# V8 SAE Feature / Circuit Ablation Controls",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Feature Ablation",
        "",
        f"- top architecture features removed: `{f['top_features']}`",
        f"- full balanced accuracy: `{f['full_balanced_accuracy']:.6f}`",
        f"- top-removed balanced accuracy: `{f['top_removed_balanced_accuracy']:.6f}`",
        f"- top feature drop: `{f['top_feature_drop']:.6f}`",
        f"- random drop mean: `{f['random_drop_mean']:.6f}`",
        f"- random drop p95: `{f['random_drop_p95']:.6f}`",
        f"- drop p-value: `{f['drop_p_value']:.6f}`",
        f"- feature ablation supported: `{f['feature_ablation_supported']}`",
        "",
        "## Edge Ablation",
        "",
        f"- edge rows: `{e['edge_rows']}`",
        f"- edge rows after top-feature removal: `{e['top_removed_edge_rows']}`",
        f"- full edge balanced accuracy: `{e['full_balanced_accuracy']:.6f}`",
        f"- top-removed edge balanced accuracy: `{e['top_removed_balanced_accuracy']:.6f}`",
        f"- top edge-feature drop: `{e['top_edge_feature_drop']:.6f}`",
        f"- random drop mean: `{e['random_drop_mean']:.6f}`",
        f"- random drop p95: `{e['random_drop_p95']:.6f}`",
        f"- drop p-value: `{e['drop_p_value']:.6f}`",
        f"- edge ablation supported: `{e['edge_ablation_supported']}`",
        "",
        "## Next Gates",
        "",
    ]
    for item in report["next_gates"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    feature_result = feature_ablation()
    edge_result = edge_ablation(feature_result["top_features"])
    status = (
        "sae_feature_and_edge_ablation_supported"
        if feature_result["feature_ablation_supported"] and edge_result["edge_ablation_supported"]
        else "sae_feature_ablation_supported_edge_ablation_open"
        if feature_result["feature_ablation_supported"]
        else "sae_edge_ablation_supported_feature_ablation_open"
        if edge_result["edge_ablation_supported"]
        else "sae_ablation_open"
    )
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "clean_read": (
            "Removing the strongest exported SAE architecture features reduces both feature-level and edge-level context "
            "separation beyond matched random removals. This supports the feature/circuit ablation gate."
            if status == "sae_feature_and_edge_ablation_supported"
            else "The ablation gate produced a split result. The supported side is recorded, and the open side needs denser "
            "feature exports, edge controls, or direct readout/hidden-state ablations."
            if status != "sae_ablation_open"
            else "The ablation gate did not beat matched random feature removals. Feature and edge separation remain supported "
            "from prior controls, while causal-style ablation support stays open."
        ),
        "feature_ablation": feature_result,
        "edge_ablation": edge_result,
        "next_gates": [
            "run direct readout / hidden-state ablations when the activation exporter can replay model internals",
            "repeat ablation after rerun_02 and prompt_set_02 SAE exports exist",
            "compare ablation effects against feature-frequency and token-window controls",
        ],
    }
    json_path = OUT_DIR / "v8_sae_ablation_controls_report.json"
    md_path = OUT_DIR / "v8_sae_ablation_controls_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
