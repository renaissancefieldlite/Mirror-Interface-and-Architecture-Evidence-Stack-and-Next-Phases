#!/usr/bin/env python3
"""Nest 1 next-wave pass.

Runs the next immediately available Nest 1 lanes on real artifacts:

- DYN: layer-trajectory peak-position controls over V8 residual traces.
- INFO/TENSOR: SVD/effective-rank controls over the Phase 6 feature matrix.
- GRAPH-lite: kNN edge recovery controls over the Phase 6 feature graph.
- TOP: honest blocked status if raw hidden-state point clouds are unavailable.

No synthetic data is generated. Nulls shuffle existing real artifacts or sample
matched random layer positions.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import deque
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PHASE6 = REPO_ROOT / "artifacts" / "v8" / "phase6_pennylane_encoding" / "v8_phase6_pennylane_encoding_data_2026-04-22.json"
DEFAULT_RESIDUAL_ROOT = REPO_ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "probe_results"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "nest1_next_wave"

EXPECTED_BRIDGE_PAIRS = [
    ("Mistral", "Hermes"),
    ("Qwen", "DeepSeek"),
    ("GLM", "Nemotron"),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def as_float(value: Any, default: float = float("nan")) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def clean_float(value: Any, digits: int = 6) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    return round(numeric, digits)


def zscore(matrix: np.ndarray) -> np.ndarray:
    mean = np.mean(matrix, axis=0)
    std = np.std(matrix, axis=0)
    std[std == 0] = 1.0
    return (matrix - mean) / std


def pairwise_distances(matrix: np.ndarray) -> np.ndarray:
    diff = matrix[:, None, :] - matrix[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=2))


def load_phase6_matrix(path: Path) -> tuple[list[str], list[str], np.ndarray]:
    data = load_json(path)
    features = list(data["features"])
    labels = [str(model["model"]) for model in data["models"]]
    rows = []
    for model in data["models"]:
        rows.append([as_float(model["normalized_features"].get(feature)) for feature in features])
    return labels, features, np.array(rows, dtype=float)


def svd_stats(matrix: np.ndarray) -> dict[str, Any]:
    centered = matrix - np.mean(matrix, axis=0)
    _, singular, _ = np.linalg.svd(centered, full_matrices=False)
    variances = singular * singular
    total = float(np.sum(variances))
    ratios = variances / total if total else np.zeros_like(variances)
    positive = ratios[ratios > 0]
    entropy = -float(np.sum(positive * np.log(positive))) if len(positive) else 0.0
    return {
        "singular_values": [clean_float(value) for value in singular],
        "variance_ratio": [clean_float(value) for value in ratios],
        "top2_variance": clean_float(np.sum(ratios[:2])),
        "effective_rank": clean_float(math.exp(entropy)),
    }


def nearest_graph_edges(labels: list[str], distances: np.ndarray, k: int = 2) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for i, label in enumerate(labels):
        order = [j for j in np.argsort(distances[i]) if j != i][:k]
        for j in order:
            edges.add(tuple(sorted((label, labels[j]))))
    return edges


def component_count(labels: list[str], edges: set[tuple[str, str]]) -> int:
    graph = {label: set() for label in labels}
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    seen = set()
    count = 0
    for label in labels:
        if label in seen:
            continue
        count += 1
        queue: deque[str] = deque([label])
        seen.add(label)
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
    return count


def graph_edge_hits(edges: set[tuple[str, str]]) -> int:
    hits = 0
    for left, right in EXPECTED_BRIDGE_PAIRS:
        hits += int(tuple(sorted((left, right))) in edges)
    return hits


def info_tensor_pass(phase6_path: Path, trials: int, seed: int) -> dict[str, Any]:
    labels, features, matrix = load_phase6_matrix(phase6_path)
    scaled = zscore(matrix)
    observed = svd_stats(scaled)
    rng = random.Random(seed)
    top2_null = []
    erank_null = []
    for _ in range(trials):
        shuffled = np.array(scaled, copy=True)
        for column in range(shuffled.shape[1]):
            values = list(shuffled[:, column])
            rng.shuffle(values)
            shuffled[:, column] = values
        stats = svd_stats(shuffled)
        top2_null.append(float(stats["top2_variance"]))
        erank_null.append(float(stats["effective_rank"]))
    top2_ge = sum(1 for value in top2_null if value >= float(observed["top2_variance"]))
    erank_le = sum(1 for value in erank_null if value <= float(observed["effective_rank"]))
    return {
        "lane": "INFO/TENSOR",
        "input": str(phase6_path),
        "control": "column-wise feature shuffle preserving each feature distribution",
        "observed": observed,
        "null": {
            "trials": trials,
            "mean_top2_variance": clean_float(np.mean(top2_null)),
            "mean_effective_rank": clean_float(np.mean(erank_null)),
            "p_top2_ge_observed": clean_float((top2_ge + 1) / (trials + 1)),
            "p_effective_rank_le_observed": clean_float((erank_le + 1) / (trials + 1)),
        },
        "models": labels,
        "features": features,
    }


def graph_lite_pass(phase6_path: Path) -> dict[str, Any]:
    labels, _, matrix = load_phase6_matrix(phase6_path)
    scaled = zscore(matrix)
    distances = pairwise_distances(scaled)
    edges = nearest_graph_edges(labels, distances, k=2)
    observed_hits = graph_edge_hits(edges)
    observed_components = component_count(labels, edges)

    null_hits = []
    null_components = []
    total = 0
    for perm in __import__("itertools").permutations(labels):
        renamed_edges = {tuple(sorted((perm[labels.index(left)], perm[labels.index(right)]))) for left, right in edges}
        null_hits.append(graph_edge_hits(renamed_edges))
        null_components.append(component_count(list(perm), renamed_edges))
        total += 1
    hit_ge = sum(1 for value in null_hits if value >= observed_hits)
    comp_le = sum(1 for value in null_components if value <= observed_components)
    return {
        "lane": "GRAPH-lite",
        "input": str(phase6_path),
        "control": "exact label permutation over kNN graph built from real Phase 6 feature geometry",
        "observed": {
            "k": 2,
            "edge_count": len(edges),
            "component_count": observed_components,
            "expected_pair_edges": f"{observed_hits}/{len(EXPECTED_BRIDGE_PAIRS)}",
            "edges": sorted("/".join(edge) for edge in edges),
        },
        "null": {
            "permutations": total,
            "mean_expected_pair_edges": clean_float(np.mean(null_hits)),
            "mean_component_count": clean_float(np.mean(null_components)),
            "p_expected_pair_edges_ge_observed": clean_float(hit_ge / total),
            "p_component_count_le_observed": clean_float(comp_le / total),
        },
    }


def residual_trajectory_rows(root: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(root.glob("*_v8_residual_trace.json")):
        data = load_json(path)
        model = str(data.get("display_name", path.stem))
        comparison = data.get("comparisons", {}).get("lattice_vs_neutral", [])
        if not comparison:
            continue
        layers = np.array([as_float(row.get("layer_index")) for row in comparison], dtype=float)
        target = np.array([as_float(row.get("target_delta_norm")) for row in comparison], dtype=float)
        last = np.array([as_float(row.get("last_delta_norm")) for row in comparison], dtype=float)
        if len(layers) == 0:
            continue
        peak_idx = int(np.nanargmax(target))
        rows.append(
            {
                "model": model,
                "layer_count": int(len(layers)),
                "target_peak_layer": int(layers[peak_idx]),
                "target_peak_fraction": float(layers[peak_idx] / max(layers[-1], 1.0)),
                "target_peak_value": float(target[peak_idx]),
                "target_auc": float(np.trapezoid(target, layers)) if len(target) > 1 else float(target[0]),
                "last_auc": float(np.trapezoid(last, layers)) if len(last) > 1 else float(last[0]),
                "target_last_auc_ratio": float(np.trapezoid(target, layers) / np.trapezoid(last, layers)) if len(target) > 1 and np.trapezoid(last, layers) else float("nan"),
            }
        )
    return rows


def dyn_pass(residual_root: Path, trials: int, seed: int) -> dict[str, Any]:
    rows = residual_trajectory_rows(residual_root)
    observed_mean_fraction = float(np.mean([row["target_peak_fraction"] for row in rows]))
    observed_late_count = sum(1 for row in rows if row["target_peak_fraction"] >= 0.9)
    rng = random.Random(seed)
    null_mean_fraction = []
    null_late_count = []
    for _ in range(trials):
        fractions = []
        late = 0
        for row in rows:
            layer_count = int(row["layer_count"])
            idx = rng.randrange(layer_count)
            fraction = idx / max(layer_count - 1, 1)
            fractions.append(fraction)
            late += int(fraction >= 0.9)
        null_mean_fraction.append(float(np.mean(fractions)))
        null_late_count.append(late)
    mean_ge = sum(1 for value in null_mean_fraction if value >= observed_mean_fraction)
    late_ge = sum(1 for value in null_late_count if value >= observed_late_count)
    return {
        "lane": "DYN",
        "input": str(residual_root),
        "control": "matched random peak-layer positions over each model's real layer count",
        "observed": {
            "model_count": len(rows),
            "mean_target_peak_fraction": clean_float(observed_mean_fraction),
            "late_peak_count_fraction_ge_0_9": f"{observed_late_count}/{len(rows)}",
            "rows": [
                {
                    **row,
                    "target_peak_fraction": clean_float(row["target_peak_fraction"]),
                    "target_peak_value": clean_float(row["target_peak_value"]),
                    "target_auc": clean_float(row["target_auc"]),
                    "last_auc": clean_float(row["last_auc"]),
                    "target_last_auc_ratio": clean_float(row["target_last_auc_ratio"]),
                }
                for row in rows
            ],
        },
        "null": {
            "trials": trials,
            "mean_peak_fraction": clean_float(np.mean(null_mean_fraction)),
            "mean_late_peak_count": clean_float(np.mean(null_late_count)),
            "p_mean_peak_fraction_ge_observed": clean_float((mean_ge + 1) / (trials + 1)),
            "p_late_peak_count_ge_observed": clean_float((late_ge + 1) / (trials + 1)),
        },
    }


def top_status(residual_root: Path) -> dict[str, Any]:
    files = sorted(residual_root.glob("*_v8_residual_trace.json"))
    raw_vector_signals = []
    for path in files:
        data = load_json(path)
        text = json.dumps(data)[:2000]
        has_raw_point_cloud = any(key in data for key in ["hidden_states", "point_clouds", "raw_hidden_vectors"])
        raw_vector_signals.append({"file": str(path), "has_raw_point_cloud": has_raw_point_cloud})
    return {
        "lane": "TOP",
        "status": "blocked_raw_point_clouds_required",
        "input_checked": str(residual_root),
        "read": (
            "Current V8 residual exports contain layer summaries and scalar deltas, "
            "not raw hidden-state point clouds. Persistent homology should wait "
            "until raw vectors are exported."
        ),
        "files_checked": len(files),
        "raw_vector_signals": raw_vector_signals,
    }


def lane_status(result: dict[str, Any]) -> str:
    if result.get("lane") == "TOP":
        return "blocked"
    null = result.get("null", {})
    p_values = [
        value for key, value in null.items()
        if key.startswith("p_") and isinstance(value, (float, int))
    ]
    if any(float(value) <= 0.05 for value in p_values):
        return "control_supported"
    return "partial_or_not_significant"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    dyn = dyn_pass(args.residual_root, args.trials, args.seed)
    info_tensor = info_tensor_pass(args.phase6, args.trials, args.seed + 1)
    graph_lite = graph_lite_pass(args.phase6)
    top = top_status(args.residual_root)
    lane_results = [dyn, info_tensor, graph_lite, top]
    lanes = []
    for result in lane_results:
        lanes.append(
            {
                "lane": result["lane"],
                "status": lane_status(result),
                "control": result.get("control", result.get("read")),
            }
        )
    return {
        "status": "completed_local_next_wave",
        "claim_boundary": (
            "Next-wave Nest 1 pass over available real artifacts. DYN, "
            "INFO/TENSOR, and GRAPH-lite run with controls; TOP is blocked "
            "until raw hidden-state point clouds are exported."
        ),
        "trials": args.trials,
        "seed": args.seed,
        "lanes": lanes,
        "results": {
            "dyn": dyn,
            "info_tensor": info_tensor,
            "graph_lite": graph_lite,
            "top": top,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Nest 1 Next-Wave Pass",
        "",
        f"Status: `{report['status']}`",
        "",
        report["claim_boundary"],
        "",
        "## Lane Summary",
        "",
        "| Lane | Status | Control / Read |",
        "| --- | --- | --- |",
    ]
    for lane in report["lanes"]:
        lines.append(f"| `{lane['lane']}` | `{lane['status']}` | {lane['control']} |")

    dyn = report["results"]["dyn"]
    lines.extend(
        [
            "",
            "## DYN Layer-Trajectory Control",
            "",
            f"- Observed mean target peak fraction: `{dyn['observed']['mean_target_peak_fraction']}`",
            f"- Observed late peak count: `{dyn['observed']['late_peak_count_fraction_ge_0_9']}`",
            f"- Null mean peak fraction: `{dyn['null']['mean_peak_fraction']}`",
            f"- Null mean late peak count: `{dyn['null']['mean_late_peak_count']}`",
            f"- p(mean peak fraction >= observed): `{dyn['null']['p_mean_peak_fraction_ge_observed']}`",
            f"- p(late peak count >= observed): `{dyn['null']['p_late_peak_count_ge_observed']}`",
            "",
            "| Model | Layer Count | Target Peak Layer | Peak Fraction | Target/Last AUC Ratio |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in dyn["observed"]["rows"]:
        lines.append(
            f"| {row['model']} | {row['layer_count']} | {row['target_peak_layer']} | "
            f"{row['target_peak_fraction']} | {row['target_last_auc_ratio']} |"
        )

    info = report["results"]["info_tensor"]
    lines.extend(
        [
            "",
            "## INFO/TENSOR Feature-Axis Control",
            "",
            f"- Observed top-2 SVD variance: `{info['observed']['top2_variance']}`",
            f"- Observed effective rank: `{info['observed']['effective_rank']}`",
            f"- Null mean top-2 variance: `{info['null']['mean_top2_variance']}`",
            f"- Null mean effective rank: `{info['null']['mean_effective_rank']}`",
            f"- p(top-2 variance >= observed): `{info['null']['p_top2_ge_observed']}`",
            f"- p(effective rank <= observed): `{info['null']['p_effective_rank_le_observed']}`",
        ]
    )

    graph = report["results"]["graph_lite"]
    lines.extend(
        [
            "",
            "## GRAPH-Lite kNN Edge Control",
            "",
            f"- Observed expected-pair edges: `{graph['observed']['expected_pair_edges']}`",
            f"- Observed component count: `{graph['observed']['component_count']}`",
            f"- Null mean expected-pair edges: `{graph['null']['mean_expected_pair_edges']}`",
            f"- p(expected-pair edges >= observed): `{graph['null']['p_expected_pair_edges_ge_observed']}`",
            f"- p(component count <= observed): `{graph['null']['p_component_count_le_observed']}`",
        ]
    )

    top = report["results"]["top"]
    lines.extend(
        [
            "",
            "## TOP Persistent-Homology Status",
            "",
            f"- Status: `{top['status']}`",
            f"- Files checked: `{top['files_checked']}`",
            f"- Read: {top['read']}",
            "",
            "## Boundary",
            "",
            "`DYN`, `INFO/TENSOR`, and `GRAPH-lite` are next-wave real-artifact passes. "
            "`TOP` is not closed because persistent homology requires raw hidden-state "
            "point clouds. `OPT`, `CTRL`, and `COMP/CAT` remain separate blocked lanes.",
            "",
        ]
    )
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def json_ready(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, dict):
        return {key: json_ready(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [json_ready(inner) for inner in value]
    return value


def run(args: argparse.Namespace) -> dict[str, Any]:
    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(args)
    (args.out_dir / "nest1_next_wave_report.json").write_text(
        json.dumps(json_ready(report), indent=2),
        encoding="utf-8",
    )
    (args.out_dir / "nest1_next_wave_report.md").write_text(
        render_markdown(report),
        encoding="utf-8",
    )
    write_csv(args.out_dir / "nest1_next_wave_lane_summary.csv", report["lanes"])
    write_csv(args.out_dir / "nest1_next_wave_dyn_rows.csv", report["results"]["dyn"]["observed"]["rows"])
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase6", type=Path, default=DEFAULT_PHASE6)
    parser.add_argument("--residual-root", type=Path, default=DEFAULT_RESIDUAL_ROOT)
    parser.add_argument("--trials", type=int, default=50000)
    parser.add_argument("--seed", type=int, default=6711)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({"status": report["status"], "out_dir": str(args.out_dir), "lanes": report["lanes"]}, indent=2))


if __name__ == "__main__":
    main()
