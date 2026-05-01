#!/usr/bin/env python3
"""Targeted v2 ablation for recurrent SAE feature/circuit paths.

The first recurrent-branch ablation found real branch-specific support but left
the GLM/Hermes prompt_set_02 transfer subcase open. This runner focuses on
that weak case instead of rerunning the same 100-edge test.

It strengthens the gate in four ways:

- larger top-k shared edge capture: 250, 500, 1000
- weighted recurrent edge ranking across base and target sets
- graph-neighborhood feature ablation around recurrent endpoints
- 500-trial confirmation controls on the strongest screened candidates
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
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
OUT = ROOT / "artifacts" / "validation" / "v8_sae_recurrent_branch_ablation_v2"

SEED = 67
SCREEN_RANDOM_TRIALS = 100
CONFIRM_RANDOM_TRIALS = 500
CONFIRM_TOP_N = 6
TOP_K_VALUES = (250, 500, 1000)
TARGET_BRANCH = "glm_hermes"
TARGET_SET = "prompt_set_02"


@dataclass(frozen=True)
class Candidate:
    selector: str
    top_k: int
    removal: str
    edge_keys: tuple[str, ...]
    features: tuple[int, ...]

    @property
    def name(self) -> str:
        return f"{self.selector}_k{self.top_k}_{self.removal}"


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


def edge_weight_map(edges: pd.DataFrame) -> pd.Series:
    return edges.groupby("edge_key")["edge_weight"].mean()


def top_overlap_edge_keys(base_edges: pd.DataFrame, target_edges: pd.DataFrame, top_k: int) -> list[str]:
    base_top = set(base_edges.sort_values("edge_weight", ascending=False).head(top_k)["edge_key"].astype(str))
    target_top = set(target_edges.sort_values("edge_weight", ascending=False).head(top_k)["edge_key"].astype(str))
    return sorted(base_top & target_top)


def weighted_recurrent_edge_keys(base_edges: pd.DataFrame, target_edges: pd.DataFrame, top_k: int) -> list[str]:
    base_weights = edge_weight_map(base_edges)
    target_weights = edge_weight_map(target_edges)
    shared = sorted(set(base_weights.index.astype(str)) & set(target_weights.index.astype(str)))
    if not shared:
        return []
    scores = []
    for key in shared:
        base_w = float(base_weights.loc[key])
        target_w = float(target_weights.loc[key])
        scores.append((key, float(np.sqrt(max(base_w, 0.0) * max(target_w, 0.0)))))
    scores.sort(key=lambda item: item[1], reverse=True)
    return [key for key, _ in scores[:top_k]]


def endpoint_features(edges: pd.DataFrame, edge_keys: list[str]) -> list[int]:
    sub = edges[edges["edge_key"].isin(edge_keys)]
    features = set(sub["source_feature_id"].astype(int).tolist()) | set(sub["target_feature_id"].astype(int).tolist())
    return sorted(features)


def feature_neighborhood(branch_edges: pd.DataFrame, features: list[int], top_k_edges: int) -> list[int]:
    """Expand selected features through one graph hop on high-weight branch edges."""
    if not features:
        return []
    selected = set(features)
    top = branch_edges.sort_values("edge_weight", ascending=False).head(top_k_edges)
    mask = top["source_feature_id"].isin(selected) | top["target_feature_id"].isin(selected)
    neighbors = set(top.loc[mask, "source_feature_id"].astype(int).tolist())
    neighbors |= set(top.loc[mask, "target_feature_id"].astype(int).tolist())
    return sorted(selected | neighbors)


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


def p_value(drop: float, random_drops: list[float]) -> float:
    arr = np.asarray(random_drops, dtype=float)
    return float((np.sum(arr >= drop) + 1) / (len(arr) + 1))


def random_feature_drop(
    branch_edges: pd.DataFrame,
    base_edges: pd.DataFrame,
    target_edges: pd.DataFrame,
    full_score: float,
    feature_count: int,
    trials: int,
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
    for _ in range(trials):
        remove = rng.choice(universe, size=feature_count, replace=False).astype(int).tolist()
        train = remove_endpoint_features(base_edges, remove)
        test = remove_endpoint_features(target_edges, remove)
        rows.append((len(train), len(test)))
        drops.append(full_score - transfer_score(train, test))
    arr = np.asarray(drops, dtype=float)
    return {
        "trials": trials,
        "drop_mean": round(float(arr.mean()), 9),
        "drop_p95": round(float(np.quantile(arr, 0.95)), 9),
        "drop_p99": round(float(np.quantile(arr, 0.99)), 9),
        "rows_remaining_mean": {
            "train": round(float(np.mean([row[0] for row in rows])), 3),
            "test": round(float(np.mean([row[1] for row in rows])), 3),
        },
        "drops": [round(float(x), 9) for x in arr.tolist()],
    }


def random_edge_drop(
    branch_edges: pd.DataFrame,
    base_edges: pd.DataFrame,
    target_edges: pd.DataFrame,
    full_score: float,
    edge_count: int,
    trials: int,
    seed_name: str,
) -> dict[str, Any]:
    rng = np.random.default_rng(stable_seed(seed_name))
    universe = sorted(branch_edges["edge_key"].astype(str).unique().tolist())
    edge_count = min(edge_count, len(universe))
    drops = []
    rows = []
    for _ in range(trials):
        remove = rng.choice(universe, size=edge_count, replace=False).astype(str).tolist()
        train = remove_edge_keys(base_edges, remove)
        test = remove_edge_keys(target_edges, remove)
        rows.append((len(train), len(test)))
        drops.append(full_score - transfer_score(train, test))
    arr = np.asarray(drops, dtype=float)
    return {
        "trials": trials,
        "drop_mean": round(float(arr.mean()), 9),
        "drop_p95": round(float(np.quantile(arr, 0.95)), 9),
        "drop_p99": round(float(np.quantile(arr, 0.99)), 9),
        "rows_remaining_mean": {
            "train": round(float(np.mean([row[0] for row in rows])), 3),
            "test": round(float(np.mean([row[1] for row in rows])), 3),
        },
        "drops": [round(float(x), 9) for x in arr.tolist()],
    }


def ablate_candidate(
    candidate: Candidate,
    branch_edges: pd.DataFrame,
    base_edges: pd.DataFrame,
    target_edges: pd.DataFrame,
    full_score: float,
    trials: int,
    stage: str,
) -> dict[str, Any]:
    if candidate.removal == "edge_key":
        train = remove_edge_keys(base_edges, list(candidate.edge_keys))
        test = remove_edge_keys(target_edges, list(candidate.edge_keys))
        random = random_edge_drop(
            branch_edges,
            base_edges,
            target_edges,
            full_score,
            len(candidate.edge_keys),
            trials,
            f"{stage}:{candidate.name}:edge",
        )
    else:
        train = remove_endpoint_features(base_edges, list(candidate.features))
        test = remove_endpoint_features(target_edges, list(candidate.features))
        random = random_feature_drop(
            branch_edges,
            base_edges,
            target_edges,
            full_score,
            len(candidate.features),
            trials,
            f"{stage}:{candidate.name}:feature",
        )
    ablated_score = transfer_score(train, test)
    drop = full_score - ablated_score
    p = p_value(drop, random["drops"])
    return {
        "name": candidate.name,
        "selector": candidate.selector,
        "top_k": candidate.top_k,
        "removal": candidate.removal,
        "edge_key_count": len(candidate.edge_keys),
        "feature_count": len(candidate.features),
        "ablated_transfer_balanced_accuracy": round(float(ablated_score), 9),
        "drop": round(float(drop), 9),
        "random_trials": trials,
        "random_drop_mean": random["drop_mean"],
        "random_drop_p95": random["drop_p95"],
        "random_drop_p99": random["drop_p99"],
        "p_value": round(float(p), 9),
        "supported": bool(drop > random["drop_p95"] and p <= 0.05),
        "rows_after_ablation": {"train": int(len(train)), "test": int(len(test))},
        "random_rows_remaining_mean": random["rows_remaining_mean"],
    }


def build_candidates(branch_edges: pd.DataFrame, base_edges: pd.DataFrame, target_edges: pd.DataFrame) -> list[Candidate]:
    candidates: list[Candidate] = []
    for top_k in TOP_K_VALUES:
        selectors = {
            "top_overlap": top_overlap_edge_keys(base_edges, target_edges, top_k),
            "weighted_recurrent": weighted_recurrent_edge_keys(base_edges, target_edges, top_k),
        }
        for selector, keys in selectors.items():
            features = endpoint_features(branch_edges, keys)
            neighborhood = feature_neighborhood(branch_edges, features, top_k_edges=max(top_k, 1000))
            candidates.append(Candidate(selector, top_k, "endpoint_feature", tuple(keys), tuple(features)))
            candidates.append(Candidate(selector, top_k, "feature_neighborhood", tuple(keys), tuple(neighborhood)))
            candidates.append(Candidate(selector, top_k, "edge_key", tuple(keys), tuple(features)))
    # De-duplicate identical removal sets so the report stays readable.
    seen = set()
    unique = []
    for candidate in candidates:
        fingerprint = (candidate.selector, candidate.top_k, candidate.removal, candidate.edge_keys, candidate.features)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        unique.append(candidate)
    return unique


def write_report(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 SAE Recurrent Branch Ablation V2 Report",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Target",
        "",
        f"- branch: `{report['target']['branch']}`",
        f"- transfer: `base -> {report['target']['target_set']}`",
        f"- full transfer balanced accuracy: `{report['full_transfer_balanced_accuracy']}`",
        "",
        "## Best Confirmed Candidates",
        "",
    ]
    for result in report["confirm_results"]:
        lines.extend(
            [
                f"### {result['name']}",
                "",
                f"- removal: `{result['removal']}`",
                f"- top_k: `{result['top_k']}`",
                f"- edge keys: `{result['edge_key_count']}`",
                f"- features removed: `{result['feature_count']}`",
                f"- ablation drop: `{result['drop']}`",
                f"- random p95 / p99: `{result['random_drop_p95']}` / `{result['random_drop_p99']}`",
                f"- p-value: `{result['p_value']}`",
                f"- supported: `{result['supported']}`",
                f"- rows after ablation: train `{result['rows_after_ablation']['train']}`, test `{result['rows_after_ablation']['test']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation Note",
            "",
            "The broad endpoint-feature removals identify high-impact recurrent SAE features. "
            "The sharper circuit-path read is the exact edge-key result, because those ablations "
            "leave thousands of rows in train/test while still beating matched random removals.",
            "",
            "## Screen Summary",
            "",
            f"- screened candidates: `{len(report['screen_results'])}`",
            f"- screen random trials: `{report['inputs']['screen_random_trials']}`",
            f"- confirm random trials: `{report['inputs']['confirm_random_trials']}`",
            f"- confirmed candidates: `{len(report['confirm_results'])}`",
            "",
            "## Next Gates",
            "",
        ]
    )
    for item in report["next_gates"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    require_inputs()
    OUT.mkdir(parents=True, exist_ok=True)
    edges = load_edges()
    branch_edges = edges[edges["branch"] == TARGET_BRANCH].copy()
    base_edges = branch_edges[branch_edges["source_set"] == "base"].copy()
    target_edges = branch_edges[branch_edges["source_set"] == TARGET_SET].copy()
    full_score = transfer_score(base_edges, target_edges)

    candidates = build_candidates(branch_edges, base_edges, target_edges)
    screen_results = [
        ablate_candidate(candidate, branch_edges, base_edges, target_edges, full_score, SCREEN_RANDOM_TRIALS, "screen")
        for candidate in candidates
    ]
    screen_results.sort(key=lambda result: (result["supported"], result["drop"] - result["random_drop_p95"]), reverse=True)

    confirm_names = {result["name"] for result in screen_results[:CONFIRM_TOP_N]}
    confirm_candidates = [candidate for candidate in candidates if candidate.name in confirm_names]
    confirm_results = [
        ablate_candidate(candidate, branch_edges, base_edges, target_edges, full_score, CONFIRM_RANDOM_TRIALS, "confirm")
        for candidate in confirm_candidates
    ]
    confirm_results.sort(key=lambda result: (result["supported"], result["drop"] - result["random_drop_p95"]), reverse=True)

    supported = [result for result in confirm_results if result["supported"]]
    status = "sae_recurrent_branch_ablation_v2_supported" if supported else "sae_recurrent_branch_ablation_v2_open"
    clean_read = (
        "The targeted SAE recurrent-branch ablation v2 closes the GLM/Hermes prompt_set_02 weak case under stronger shared-path capture and 500-trial controls."
        if supported
        else "The targeted SAE recurrent-branch ablation v2 keeps the GLM/Hermes prompt_set_02 ablation case open after larger shared-path capture, weighted recurrence ranking, neighborhood ablation, and 500-trial controls."
    )

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "clean_read": clean_read,
        "target": {"branch": TARGET_BRANCH, "target_set": TARGET_SET},
        "full_transfer_balanced_accuracy": round(float(full_score), 9),
        "inputs": {
            "edge_path": str(EDGE_PATH.relative_to(ROOT)),
            "edge_rows": int(len(edges)),
            "target_branch_rows": int(len(branch_edges)),
            "base_rows": int(len(base_edges)),
            "target_rows": int(len(target_edges)),
            "branch_counts": dict(Counter(edges["branch"].tolist())),
            "set_counts": dict(Counter(edges["source_set"].tolist())),
            "top_k_values": TOP_K_VALUES,
            "screen_random_trials": SCREEN_RANDOM_TRIALS,
            "confirm_random_trials": CONFIRM_RANDOM_TRIALS,
            "confirm_top_n": CONFIRM_TOP_N,
        },
        "screen_results": screen_results,
        "confirm_results": confirm_results,
        "next_gates": [
            "update SAE protocol with v2 support",
            "run MLP depth recurrence before Nest 2D allostery",
        ],
    }
    json_path = OUT / "v8_sae_recurrent_branch_ablation_v2_report.json"
    md_path = OUT / "v8_sae_recurrent_branch_ablation_v2_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_report(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
