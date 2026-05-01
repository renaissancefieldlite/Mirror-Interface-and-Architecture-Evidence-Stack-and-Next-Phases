#!/usr/bin/env python3
"""Ablate recurrent SAE feature/circuit paths across recurrence branches.

The feature-edge recurrence gate identified repeated adjacent-layer SAE edge
paths across base, rerun_02, and prompt_set_02. This runner tests whether
removing those recurrent paths moves the branch readout more than matched
random feature or edge removals.

It operates on the compact recurrent edge export, so it stays auditable:

- recurrent endpoint-feature ablation removes rows touching features that
  appear in top shared base->target recurrent edge paths
- recurrent edge-key ablation removes the exact shared edge keys
- matched random controls use the same number of features or edge keys
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
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
EDGE_PATH = (
    ROOT
    / "artifacts"
    / "validation"
    / "v8_sae_feature_edge_recurrence"
    / "v8_sae_feature_edge_recurrence_edges.csv"
)
OUT = ROOT / "artifacts" / "validation" / "v8_sae_recurrent_branch_ablation"

SEED = 67
RANDOM_TRIALS = 100
TOP_K_SHARED_EDGES = 100
BRANCHES = ("glm_hermes", "gemma")
TARGETS = ("rerun_02", "prompt_set_02")


def stable_seed(name: str) -> int:
    return SEED + sum((idx + 1) * ord(char) for idx, char in enumerate(name))


def require_inputs() -> None:
    if not EDGE_PATH.exists():
        raise SystemExit(f"Missing recurrent edge export: {EDGE_PATH}")


def load_edges() -> pd.DataFrame:
    edges = pd.read_csv(EDGE_PATH)
    required = {
        "branch",
        "source_set",
        "model",
        "context",
        "token_region",
        "source_layer",
        "source_feature_id",
        "target_layer",
        "target_feature_id",
        "edge_weight",
        "edge_key",
    }
    missing = sorted(required - set(edges.columns))
    if missing:
        raise ValueError(f"Recurrent edge export missing columns: {missing}")
    edges = edges.copy()
    edges["source_layer"] = edges["source_layer"].astype(int)
    edges["target_layer"] = edges["target_layer"].astype(int)
    edges["source_feature_id"] = edges["source_feature_id"].astype(int)
    edges["target_feature_id"] = edges["target_feature_id"].astype(int)
    edges["edge_weight"] = edges["edge_weight"].astype(float)
    edges["layer_gap"] = edges["target_layer"] - edges["source_layer"]
    edges["same_feature"] = (edges["source_feature_id"] == edges["target_feature_id"]).astype(int)
    edges["feature_pair"] = edges["source_feature_id"].astype(str) + "->" + edges["target_feature_id"].astype(str)
    edges["layer_pair"] = edges["source_layer"].astype(str) + "->" + edges["target_layer"].astype(str)
    edges["log_edge_weight"] = np.log1p(np.maximum(edges["edge_weight"].to_numpy(), 0.0))
    return edges


def matrix(edges: pd.DataFrame, columns: list[str] | None = None) -> tuple[pd.DataFrame, list[str]]:
    base = edges[
        [
            "edge_weight",
            "log_edge_weight",
            "source_layer",
            "target_layer",
            "layer_gap",
            "same_feature",
            "model",
            "token_region",
            "source_feature_id",
            "target_feature_id",
            "feature_pair",
            "layer_pair",
        ]
    ].copy()
    x = pd.get_dummies(
        base,
        columns=["model", "token_region", "source_feature_id", "target_feature_id", "feature_pair", "layer_pair"],
        dtype=float,
    )
    if columns is None:
        return x, list(x.columns)
    return x.reindex(columns=columns, fill_value=0.0), columns


def transfer_score(train_edges: pd.DataFrame, test_edges: pd.DataFrame) -> float:
    if len(train_edges) < 120 or len(test_edges) < 120:
        return 0.0
    if len(set(train_edges["context"])) < 3 or len(set(test_edges["context"])) < 3:
        return 0.0
    train_x, columns = matrix(train_edges)
    test_x, _ = matrix(test_edges, columns)
    train_y = train_edges["context"].to_numpy()
    test_y = test_edges["context"].to_numpy()
    clf = make_pipeline(StandardScaler(with_mean=False), LogisticRegression(max_iter=1000, random_state=SEED))
    clf.fit(train_x.to_numpy(dtype=float), train_y)
    return float(balanced_accuracy_score(test_y, clf.predict(test_x.to_numpy(dtype=float))))


def top_shared_edge_keys(base_edges: pd.DataFrame, target_edges: pd.DataFrame, top_k: int) -> list[str]:
    base_top = set(
        base_edges.sort_values("edge_weight", ascending=False).head(top_k)["edge_key"].astype(str).tolist()
    )
    target_top = set(
        target_edges.sort_values("edge_weight", ascending=False).head(top_k)["edge_key"].astype(str).tolist()
    )
    shared = sorted(base_top & target_top)
    return shared


def endpoint_features(edges: pd.DataFrame, edge_keys: list[str]) -> list[int]:
    sub = edges[edges["edge_key"].isin(edge_keys)]
    features = set(sub["source_feature_id"].astype(int).tolist()) | set(sub["target_feature_id"].astype(int).tolist())
    return sorted(features)


def remove_endpoint_features(edges: pd.DataFrame, features: list[int]) -> pd.DataFrame:
    if not features:
        return edges.copy()
    feature_set = set(features)
    return edges[
        ~edges["source_feature_id"].isin(feature_set)
        & ~edges["target_feature_id"].isin(feature_set)
    ].copy()


def remove_edge_keys(edges: pd.DataFrame, edge_keys: list[str]) -> pd.DataFrame:
    if not edge_keys:
        return edges.copy()
    return edges[~edges["edge_key"].isin(set(edge_keys))].copy()


def random_feature_drop(
    branch_edges: pd.DataFrame,
    base_edges: pd.DataFrame,
    target_edges: pd.DataFrame,
    full_score: float,
    feature_count: int,
    seed_name: str,
) -> dict[str, Any]:
    rng = np.random.default_rng(stable_seed(seed_name))
    universe = sorted(
        set(branch_edges["source_feature_id"].astype(int).tolist())
        | set(branch_edges["target_feature_id"].astype(int).tolist())
    )
    feature_count = min(feature_count, len(universe))
    drops = []
    rows = []
    for _ in range(RANDOM_TRIALS):
        remove = rng.choice(universe, size=feature_count, replace=False).astype(int).tolist()
        train = remove_endpoint_features(base_edges, remove)
        test = remove_endpoint_features(target_edges, remove)
        rows.append({"train": int(len(train)), "test": int(len(test))})
        drops.append(full_score - transfer_score(train, test))
    arr = np.asarray(drops, dtype=float)
    return {
        "drop_mean": round(float(arr.mean()), 9),
        "drop_p95": round(float(np.quantile(arr, 0.95)), 9),
        "rows_remaining_mean": {
            "train": round(float(np.mean([row["train"] for row in rows])), 3),
            "test": round(float(np.mean([row["test"] for row in rows])), 3),
        },
        "drops": [round(float(x), 9) for x in arr.tolist()],
    }


def random_edge_drop(
    branch_edges: pd.DataFrame,
    base_edges: pd.DataFrame,
    target_edges: pd.DataFrame,
    full_score: float,
    edge_count: int,
    seed_name: str,
) -> dict[str, Any]:
    rng = np.random.default_rng(stable_seed(seed_name))
    universe = sorted(branch_edges["edge_key"].astype(str).unique().tolist())
    edge_count = min(edge_count, len(universe))
    drops = []
    rows = []
    for _ in range(RANDOM_TRIALS):
        remove = rng.choice(universe, size=edge_count, replace=False).astype(str).tolist()
        train = remove_edge_keys(base_edges, remove)
        test = remove_edge_keys(target_edges, remove)
        rows.append({"train": int(len(train)), "test": int(len(test))})
        drops.append(full_score - transfer_score(train, test))
    arr = np.asarray(drops, dtype=float)
    return {
        "drop_mean": round(float(arr.mean()), 9),
        "drop_p95": round(float(np.quantile(arr, 0.95)), 9),
        "rows_remaining_mean": {
            "train": round(float(np.mean([row["train"] for row in rows])), 3),
            "test": round(float(np.mean([row["test"] for row in rows])), 3),
        },
        "drops": [round(float(x), 9) for x in arr.tolist()],
    }


def p_value(drop: float, random_drops: list[float]) -> float:
    arr = np.asarray(random_drops, dtype=float)
    return float((np.sum(arr >= drop) + 1) / (len(arr) + 1))


def score_pair(edges: pd.DataFrame, branch: str, target: str) -> dict[str, Any]:
    branch_edges = edges[edges["branch"] == branch].copy()
    base_edges = branch_edges[branch_edges["source_set"] == "base"].copy()
    target_edges = branch_edges[branch_edges["source_set"] == target].copy()
    full_score = transfer_score(base_edges, target_edges)
    shared_keys = top_shared_edge_keys(base_edges, target_edges, TOP_K_SHARED_EDGES)
    features = endpoint_features(branch_edges, shared_keys)

    feature_train = remove_endpoint_features(base_edges, features)
    feature_test = remove_endpoint_features(target_edges, features)
    feature_score = transfer_score(feature_train, feature_test)
    feature_drop = full_score - feature_score
    feature_random = random_feature_drop(
        branch_edges,
        base_edges,
        target_edges,
        full_score,
        len(features),
        f"{branch}:{target}:feature",
    )
    feature_p = p_value(feature_drop, feature_random["drops"])

    edge_train = remove_edge_keys(base_edges, shared_keys)
    edge_test = remove_edge_keys(target_edges, shared_keys)
    edge_score = transfer_score(edge_train, edge_test)
    edge_drop = full_score - edge_score
    edge_random = random_edge_drop(
        branch_edges,
        base_edges,
        target_edges,
        full_score,
        len(shared_keys),
        f"{branch}:{target}:edge",
    )
    edge_p = p_value(edge_drop, edge_random["drops"])

    return {
        "full_transfer_balanced_accuracy": round(full_score, 9),
        "shared_top_edge_count": len(shared_keys),
        "endpoint_feature_count": len(features),
        "endpoint_features": features,
        "feature_endpoint_ablation": {
            "ablated_transfer_balanced_accuracy": round(feature_score, 9),
            "drop": round(feature_drop, 9),
            "random_drop_mean": feature_random["drop_mean"],
            "random_drop_p95": feature_random["drop_p95"],
            "p_value": round(feature_p, 9),
            "supported": bool(feature_drop > feature_random["drop_p95"] and feature_p <= 0.05),
            "rows_after_ablation": {"train": int(len(feature_train)), "test": int(len(feature_test))},
            "random_rows_remaining_mean": feature_random["rows_remaining_mean"],
        },
        "edge_key_ablation": {
            "ablated_transfer_balanced_accuracy": round(edge_score, 9),
            "drop": round(edge_drop, 9),
            "random_drop_mean": edge_random["drop_mean"],
            "random_drop_p95": edge_random["drop_p95"],
            "p_value": round(edge_p, 9),
            "supported": bool(edge_drop > edge_random["drop_p95"] and edge_p <= 0.05),
            "rows_after_ablation": {"train": int(len(edge_train)), "test": int(len(edge_test))},
            "random_rows_remaining_mean": edge_random["rows_remaining_mean"],
        },
    }


def write_report(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 SAE Recurrent Branch Ablation Report",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Pair Results",
        "",
    ]
    for branch, branch_results in report["pairs"].items():
        lines.append(f"### {branch}")
        lines.append("")
        for target, result in branch_results.items():
            f = result["feature_endpoint_ablation"]
            e = result["edge_key_ablation"]
            lines.extend(
                [
                    f"#### base_to_{target}",
                    "",
                    f"- full transfer balanced accuracy: `{result['full_transfer_balanced_accuracy']}`",
                    f"- shared top edge count: `{result['shared_top_edge_count']}`",
                    f"- endpoint feature count: `{result['endpoint_feature_count']}`",
                    f"- endpoint-feature ablation drop: `{f['drop']}`, random p95 `{f['random_drop_p95']}`, p `{f['p_value']}`, supported `{f['supported']}`",
                    f"- edge-key ablation drop: `{e['drop']}`, random p95 `{e['random_drop_p95']}`, p `{e['p_value']}`, supported `{e['supported']}`",
                    "",
                ]
            )
    lines.extend(["## Inputs", ""])
    for key, value in report["inputs"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Next Gates", ""])
    for item in report["next_gates"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    require_inputs()
    OUT.mkdir(parents=True, exist_ok=True)
    edges = load_edges()
    pairs = {branch: {target: score_pair(edges, branch, target) for target in TARGETS} for branch in BRANCHES}
    supported_pairs = {
        branch: {
            target: (
                result["feature_endpoint_ablation"]["supported"]
                or result["edge_key_ablation"]["supported"]
            )
            for target, result in branch_pairs.items()
        }
        for branch, branch_pairs in pairs.items()
    }
    any_supported = any(any(targets.values()) for targets in supported_pairs.values())
    all_supported = all(all(targets.values()) for targets in supported_pairs.values())
    status = (
        "sae_recurrent_branch_ablation_supported"
        if all_supported
        else "sae_recurrent_branch_ablation_partial"
        if any_supported
        else "sae_recurrent_branch_ablation_open"
    )
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "clean_read": (
            "Direct SAE recurrent-branch ablation is supported across the tested branch/target pairs. "
            "Removing recurrent feature or edge paths moves transfer readout beyond matched random removals."
            if status == "sae_recurrent_branch_ablation_supported"
            else "Direct SAE recurrent-branch ablation produced a partial read. The report identifies which recurrent feature or edge removals move transfer readout beyond matched random controls and which branches remain descriptive at this gate."
            if status == "sae_recurrent_branch_ablation_partial"
            else "Direct SAE recurrent-branch ablation remains open at this gate. The recurrent edge paths are measured and transfer-supported from the prior gate, while this run did not show drop beyond matched random removals."
        ),
        "inputs": {
            "edge_path": str(EDGE_PATH.relative_to(ROOT)),
            "edge_rows": int(len(edges)),
            "branch_counts": dict(Counter(edges["branch"].tolist())),
            "set_counts": dict(Counter(edges["source_set"].tolist())),
            "random_trials": RANDOM_TRIALS,
            "top_k_shared_edges": TOP_K_SHARED_EDGES,
        },
        "pairs": pairs,
        "supported_pairs": supported_pairs,
        "next_gates": [
            "run MLP depth recurrence",
            "move to Nest 2D allostery after MLP depth recurrence is logged",
            "keep ABC / D / V5 prelude provenance linked as the sequence-scoring origin scaffold",
        ],
    }
    json_path = OUT / "v8_sae_recurrent_branch_ablation_report.json"
    md_path = OUT / "v8_sae_recurrent_branch_ablation_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_report(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
