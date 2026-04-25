#!/usr/bin/env python3
"""Nest 1 real-trace foundation pass.

This runner keeps the Nest 1 work grounded in existing project artifacts. It
does not generate toy rows. It reads real V8 feature, residual-trace, rerun,
and hardware-repeatability artifacts and produces a draft foundation report for
the major deep-learning math branches.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PHASE6 = REPO_ROOT / "artifacts" / "v8" / "phase6_pennylane_encoding" / "v8_phase6_pennylane_encoding_data_2026-04-22.json"
DEFAULT_PHASE2 = REPO_ROOT / "artifacts" / "v8" / "phase2_variance_pack" / "v8_phase2_variance_pack_data_2026-04-21.json"
DEFAULT_PHASE5 = REPO_ROOT / "artifacts" / "v8" / "phase5_internal_bridge" / "v8_phase5_internal_bridge_pack_data_2026-04-22.json"
DEFAULT_PHASE9D = REPO_ROOT / "artifacts" / "v8" / "phase9d_pennylane_remote_repeat" / "v8_phase9d_pennylane_remote_repeat_data_2026-04-22.json"
DEFAULT_RESIDUAL_ROOT = REPO_ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "probe_results"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "nest1_real_trace_foundation"

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


def clean_float(value: float, digits: int = 6) -> float | None:
    if not math.isfinite(float(value)):
        return None
    return round(float(value), digits)


def zscore(matrix: np.ndarray) -> np.ndarray:
    mean = np.mean(matrix, axis=0)
    std = np.std(matrix, axis=0)
    std[std == 0] = 1.0
    return (matrix - mean) / std


def pairwise_distances(matrix: np.ndarray) -> np.ndarray:
    diff = matrix[:, None, :] - matrix[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=2))


def cosine_similarity_matrix(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1)
    norms[norms == 0] = 1.0
    normalized = matrix / norms[:, None]
    return normalized @ normalized.T


def effective_rank(variance_ratio: np.ndarray) -> float:
    positive = variance_ratio[variance_ratio > 0]
    if len(positive) == 0:
        return 0.0
    entropy = -float(np.sum(positive * np.log(positive)))
    return float(np.exp(entropy))


def load_phase6_matrix(path: Path) -> tuple[list[str], list[str], np.ndarray, list[dict[str, Any]]]:
    data = load_json(path)
    features = list(data["features"])
    rows = []
    models = []
    metadata = []
    for model in data["models"]:
        models.append(str(model["model"]))
        rows.append([as_float(model["normalized_features"].get(feature)) for feature in features])
        metadata.append(
            {
                "model": model["model"],
                "path_archetype": model["raw"].get("path_archetype"),
                "dominant_anchor": model["raw"].get("dominant_anchor"),
                "variance_note": model["raw"].get("variance_note"),
            }
        )
    return models, features, np.array(rows, dtype=float), metadata


def pca_summary(matrix: np.ndarray) -> dict[str, Any]:
    centered = matrix - np.mean(matrix, axis=0)
    _, singular_values, vh = np.linalg.svd(centered, full_matrices=False)
    variances = singular_values * singular_values
    total = float(np.sum(variances))
    variance_ratio = variances / total if total else np.zeros_like(variances)
    coordinates = centered @ vh[: min(3, len(vh))].T
    return {
        "singular_values": [clean_float(v) for v in singular_values],
        "variance_ratio": [clean_float(v) for v in variance_ratio],
        "top1_variance_ratio": clean_float(variance_ratio[0]) if len(variance_ratio) else None,
        "top2_variance_ratio": clean_float(np.sum(variance_ratio[:2])) if len(variance_ratio) else None,
        "effective_rank": clean_float(effective_rank(variance_ratio)),
        "coordinates": coordinates,
    }


def nearest_neighbors(models: list[str], distances: np.ndarray) -> list[dict[str, Any]]:
    rows = []
    for i, model in enumerate(models):
        order = np.argsort(distances[i])
        nearest = [j for j in order if j != i]
        rows.append(
            {
                "model": model,
                "nearest_model": models[nearest[0]],
                "nearest_distance": clean_float(distances[i, nearest[0]]),
                "second_nearest_model": models[nearest[1]] if len(nearest) > 1 else None,
                "second_nearest_distance": clean_float(distances[i, nearest[1]]) if len(nearest) > 1 else None,
            }
        )
    return rows


def bridge_pair_checks(models: list[str], distances: np.ndarray) -> list[dict[str, Any]]:
    index = {model: i for i, model in enumerate(models)}
    checks = []
    for left, right in EXPECTED_BRIDGE_PAIRS:
        if left not in index or right not in index:
            checks.append({"pair": f"{left}/{right}", "status": "missing_model"})
            continue
        left_i = index[left]
        right_i = index[right]
        left_order = [j for j in np.argsort(distances[left_i]) if j != left_i]
        right_order = [j for j in np.argsort(distances[right_i]) if j != right_i]
        left_rank = left_order.index(right_i) + 1
        right_rank = right_order.index(left_i) + 1
        checks.append(
            {
                "pair": f"{left}/{right}",
                "distance": clean_float(distances[left_i, right_i]),
                "left_rank_of_right": left_rank,
                "right_rank_of_left": right_rank,
                "mutual_nearest": left_rank == 1 and right_rank == 1,
                "within_top2_both_directions": left_rank <= 2 and right_rank <= 2,
            }
        )
    return checks


def knn_components(models: list[str], distances: np.ndarray, k: int = 2) -> dict[str, Any]:
    graph: dict[str, set[str]] = {model: set() for model in models}
    for i, model in enumerate(models):
        order = [j for j in np.argsort(distances[i]) if j != i][:k]
        for j in order:
            graph[model].add(models[j])
            graph[models[j]].add(model)

    seen = set()
    components = []
    for model in models:
        if model in seen:
            continue
        queue: deque[str] = deque([model])
        seen.add(model)
        component = []
        while queue:
            current = queue.popleft()
            component.append(current)
            for neighbor in sorted(graph[current]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append(sorted(component))

    edge_set = {tuple(sorted((left, right))) for left, neighbors in graph.items() for right in neighbors}
    expected_edges = []
    for left, right in EXPECTED_BRIDGE_PAIRS:
        expected_edges.append(
            {
                "pair": f"{left}/{right}",
                "present_as_knn_edge": tuple(sorted((left, right))) in edge_set,
            }
        )
    return {
        "k": k,
        "edge_count": len(edge_set),
        "components": components,
        "component_count": len(components),
        "expected_pair_edges": expected_edges,
    }


def phase6_rows(models: list[str], features: list[str], matrix: np.ndarray, metadata: list[dict[str, Any]], pca_coords: np.ndarray) -> list[dict[str, Any]]:
    rows = []
    for i, model in enumerate(models):
        row: dict[str, Any] = {"model": model}
        row.update(metadata[i])
        for feature, value in zip(features, matrix[i], strict=True):
            row[feature] = clean_float(value)
        if pca_coords.size:
            for axis in range(pca_coords.shape[1]):
                row[f"pc{axis + 1}"] = clean_float(pca_coords[i, axis])
        rows.append(row)
    return rows


def phase2_summary(path: Path) -> dict[str, Any]:
    data = load_json(path)
    models = data.get("models", [])
    exact = [model["display_name"] for model in models if model.get("rerun_exact_after_baseline")]
    live_variance = data.get("only_live_variance_row")
    target_stds = [as_float(model.get("target_std")) for model in models]
    last_stds = [as_float(model.get("last_std")) for model in models]
    return {
        "model_count": len(models),
        "exact_after_baseline_count": len(exact),
        "exact_after_baseline_models": exact,
        "only_live_variance_row": live_variance,
        "mean_target_std": clean_float(np.nanmean(target_stds)) if target_stds else None,
        "mean_last_std": clean_float(np.nanmean(last_stds)) if last_stds else None,
        "all_target_layers_stable": bool(data.get("all_target_layers_stable_across_all_runs")),
        "rerun_exact_rate": clean_float(len(exact) / len(models)) if models else None,
    }


def topography_rows(path: Path) -> list[dict[str, Any]]:
    data = load_json(path)
    rows = []
    for model in data.get("models", []):
        anchor_values = model.get("anchor_values", {})
        rows.append(
            {
                "model": model.get("display_name"),
                "dominant_anchor": model.get("dominant_anchor"),
                "dominant_layer": model.get("dominant_layer"),
                "dominant_delta": model.get("dominant_delta"),
                "path_archetype": model.get("path_archetype"),
                "top3_sequence": " > ".join(model.get("top3_sequence", [])),
                "anchor_layer_span": model.get("anchor_layer_span"),
                "target_to_context": model.get("target_to_context"),
                "target_to_surround": model.get("target_to_surround"),
                "last_to_target": model.get("last_to_target"),
                "overlap_count": model.get("overlap_count"),
                "overlap_jaccard": model.get("overlap_jaccard"),
                "early_delta": anchor_values.get("early"),
                "mid_delta": anchor_values.get("mid"),
                "pre_delta": anchor_values.get("pre"),
                "target_delta": anchor_values.get("target"),
                "post_delta": anchor_values.get("post"),
                "last_delta": anchor_values.get("last"),
            }
        )
    return rows


def topography_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    anchor_counts = Counter(str(row.get("dominant_anchor")) for row in rows)
    archetype_counts = Counter(str(row.get("path_archetype")) for row in rows)
    overlaps = [as_float(row.get("overlap_jaccard")) for row in rows]
    target_to_context = [as_float(row.get("target_to_context")) for row in rows]
    return {
        "models": len(rows),
        "dominant_anchor_counts": dict(anchor_counts),
        "path_archetype_counts": dict(archetype_counts),
        "mean_overlap_jaccard": clean_float(np.nanmean(overlaps)) if overlaps else None,
        "mean_target_to_context": clean_float(np.nanmean(target_to_context)) if target_to_context else None,
    }


def residual_trace_rows(root: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(root.glob("*_v8_residual_trace.json")):
        data = load_json(path)
        model = str(data.get("display_name", path.stem))
        comparisons = data.get("comparisons", {}).get("lattice_vs_neutral", [])
        if not comparisons:
            continue
        layers = np.array([as_float(item.get("layer_index")) for item in comparisons], dtype=float)
        target = np.array([as_float(item.get("target_delta_norm")) for item in comparisons], dtype=float)
        last = np.array([as_float(item.get("last_delta_norm")) for item in comparisons], dtype=float)
        cosines = np.array([as_float(item.get("target_cosine")) for item in comparisons], dtype=float)
        if len(target) == 0:
            continue
        target_peak_idx = int(np.nanargmax(target))
        last_peak_idx = int(np.nanargmax(last))
        target_auc = float(np.trapezoid(target, layers)) if len(target) > 1 else float(target[0])
        last_auc = float(np.trapezoid(last, layers)) if len(last) > 1 else float(last[0])
        roughness = float(np.nanmean(np.abs(np.diff(target)))) if len(target) > 1 else 0.0
        rows.append(
            {
                "model": model,
                "layer_count": int(len(target)),
                "target_peak_layer": int(layers[target_peak_idx]),
                "target_peak_value": clean_float(target[target_peak_idx]),
                "last_peak_layer": int(layers[last_peak_idx]),
                "last_peak_value": clean_float(last[last_peak_idx]),
                "target_last_auc_ratio": clean_float(target_auc / last_auc) if last_auc else None,
                "target_peak_layer_fraction": clean_float(layers[target_peak_idx] / max(layers[-1], 1.0)),
                "target_trajectory_roughness": clean_float(roughness),
                "mean_target_cosine": clean_float(np.nanmean(cosines)),
            }
        )
    return rows


def hardware_rows(path: Path) -> list[dict[str, Any]]:
    data = load_json(path)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pass_item in data.get("passes", []):
        label = pass_item.get("label")
        backend = pass_item.get("backend", {}).get("name")
        for result in pass_item.get("circuit_results", []):
            item = dict(result)
            item["pass_label"] = label
            item["backend_name"] = backend
            grouped[str(result.get("name"))].append(item)

    rows = []
    for name, items in sorted(grouped.items()):
        parities = np.array([as_float(item.get("parity_expectation")) for item in items], dtype=float)
        bitstrings = [str(item.get("dominant_bitstring")) for item in items]
        signs = [1 if value > 0 else -1 if value < 0 else 0 for value in parities]
        nonzero_signs = [sign for sign in signs if sign != 0]
        rows.append(
            {
                "circuit": name,
                "passes": len(items),
                "backends": ",".join(sorted({str(item.get("backend_name")) for item in items})),
                "mean_parity": clean_float(np.nanmean(parities)),
                "std_parity": clean_float(np.nanstd(parities)),
                "min_parity": clean_float(np.nanmin(parities)),
                "max_parity": clean_float(np.nanmax(parities)),
                "sign_stable": len(set(nonzero_signs)) <= 1,
                "dominant_bitstring_mode": Counter(bitstrings).most_common(1)[0][0] if bitstrings else None,
                "dominant_bitstring_counts": dict(Counter(bitstrings)),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
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


def build_report(
    phase6_path: Path,
    phase2_path: Path,
    phase5_path: Path,
    phase9d_path: Path,
    residual_root: Path,
) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    models, features, matrix, metadata = load_phase6_matrix(phase6_path)
    scaled = zscore(matrix)
    distances = pairwise_distances(scaled)
    cosines = cosine_similarity_matrix(scaled)
    pca = pca_summary(scaled)
    feature_rows = phase6_rows(models, features, matrix, metadata, np.array(pca["coordinates"]))
    nn_rows = nearest_neighbors(models, distances)
    bridge_checks = bridge_pair_checks(models, distances)
    graph = knn_components(models, distances, k=2)
    phase2 = phase2_summary(phase2_path)
    topography = topography_rows(phase5_path)
    layer_rows = residual_trace_rows(residual_root)
    hardware = hardware_rows(phase9d_path)

    bridge_top2_hits = sum(1 for item in bridge_checks if item.get("within_top2_both_directions"))
    mutual_hits = sum(1 for item in bridge_checks if item.get("mutual_nearest"))
    sign_stable_count = sum(1 for item in hardware if item["sign_stable"])
    feature_circuits = [item for item in hardware if str(item["circuit"]).startswith("phase6_feature")]
    feature_sign_stable = sum(1 for item in feature_circuits if item["sign_stable"])

    branch_results = [
        {
            "branch": "linear_algebra_geometry",
            "status": "real_trace_run",
            "input": str(phase6_path),
            "read": "Phase 6 normalized feature matrix supports PCA/SVD, pairwise distance, cosine, and bridge-pair checks.",
            "metrics": {
                "models": len(models),
                "features": len(features),
                "top2_variance_ratio": pca["top2_variance_ratio"],
                "effective_rank": pca["effective_rank"],
                "expected_pairs_top2_hits": f"{bridge_top2_hits}/{len(EXPECTED_BRIDGE_PAIRS)}",
                "expected_pairs_mutual_nearest_hits": f"{mutual_hits}/{len(EXPECTED_BRIDGE_PAIRS)}",
            },
        },
        {
            "branch": "tensor_information",
            "status": "real_trace_run",
            "input": str(phase6_path),
            "read": "Model x feature matrix gives a real tensor/information summary, but raw activation tensors would strengthen this lane.",
            "metrics": {
                "matrix_shape": [int(matrix.shape[0]), int(matrix.shape[1])],
                "singular_values": pca["singular_values"],
                "variance_ratio": pca["variance_ratio"],
            },
        },
        {
            "branch": "statistics_probability",
            "status": "real_trace_run",
            "input": str(phase2_path),
            "read": "Phase 2 rerun matrix remains the strongest real STAT/PROB surface.",
            "metrics": phase2,
        },
        {
            "branch": "graph_topology_lite",
            "status": "real_trace_run_limited",
            "input": str(phase6_path),
            "read": "KNN graph over real feature vectors is a topology-lite pass; stronger topology needs raw hidden-state point clouds.",
            "metrics": graph,
        },
        {
            "branch": "topography_bridge",
            "status": "real_trace_run",
            "input": str(phase5_path),
            "read": "Phase 5 context-to-readout anchors give a real topographic bridge over internal model traces.",
            "metrics": topography_summary(topography),
        },
        {
            "branch": "dynamical_systems",
            "status": "real_trace_run",
            "input": str(residual_root),
            "read": "Layerwise target/control delta trajectories provide a real dynamics-over-depth pass.",
            "metrics": {
                "models": len(layer_rows),
                "target_peak_layers": {row["model"]: row["target_peak_layer"] for row in layer_rows},
                "mean_target_peak_layer_fraction": clean_float(np.mean([row["target_peak_layer_fraction"] for row in layer_rows])),
            },
        },
        {
            "branch": "numerical_group_symmetry",
            "status": "real_hardware_run",
            "input": str(phase9d_path),
            "read": "Phase 9D hardware repeatability gives a real numerical/backend and sign-symmetry surface.",
            "metrics": {
                "circuits": len(hardware),
                "sign_stable_circuits": f"{sign_stable_count}/{len(hardware)}",
                "phase6_feature_sign_stable": f"{feature_sign_stable}/{len(feature_circuits)}",
            },
        },
        {
            "branch": "optimization",
            "status": "blocked_new_benchmark_needed",
            "input": None,
            "read": "Needs a declared mirror-guided optimization benchmark against naive/random/standard baselines.",
            "metrics": {},
        },
        {
            "branch": "control_theory",
            "status": "blocked_trace_needed",
            "input": None,
            "read": "Needs exported real LSPS/Oracle transition traces.",
            "metrics": {},
        },
        {
            "branch": "category_composition",
            "status": "design_lane",
            "input": None,
            "read": "Needs a measured transfer test showing structure preserved between two real nests.",
            "metrics": {},
        },
    ]

    report = {
        "status": "completed_bounded_evidence_pack",
        "claim_boundary": "Bounded Nest 1 foundation pass over existing AI and hardware artifacts; not a final universal-claim layer.",
        "inputs": {
            "phase6": str(phase6_path),
            "phase2": str(phase2_path),
            "phase5": str(phase5_path),
            "phase9d": str(phase9d_path),
            "residual_root": str(residual_root),
        },
        "branch_results": branch_results,
        "nearest_neighbors": nn_rows,
        "bridge_pair_checks": bridge_checks,
        "hardware_summary": hardware,
        "topography_summary": topography,
        "layer_dynamics_summary": layer_rows,
        "boundary": (
            "This uses real exported V8 and hardware artifacts. Some lanes are limited by "
            "the currently exported scalar summaries and still need raw hidden-state point "
            "clouds, LSPS traces, or new benchmarks before stronger claims."
        ),
    }
    tables = {
        "feature_matrix": feature_rows,
        "nearest_neighbors": nn_rows,
        "topography_bridge": topography,
        "layer_dynamics": layer_rows,
        "hardware_signs": hardware,
    }
    # Keep large coordinates out of the JSON report summary.
    for item in branch_results:
        if item["branch"] == "tensor_information":
            item["metrics"]["coordinates_basis_note"] = "PCA coordinates written in feature matrix CSV."
    return report, tables


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Nest 1 Real-Trace Foundation Report",
        "",
        f"Status: `{report['status']}`",
        "",
        report["claim_boundary"],
        "",
        "## Inputs",
        "",
    ]
    for label, path in report["inputs"].items():
        lines.append(f"- `{label}`: `{path}`")

    lines.extend(
        [
            "",
            "## Branch Results",
            "",
            "| Branch | Status | Read | Key Metrics |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in report["branch_results"]:
        metrics = "; ".join(f"{key}={value}" for key, value in item["metrics"].items() if key not in {"singular_values", "variance_ratio", "components", "expected_pair_edges"})
        lines.append(f"| `{item['branch']}` | `{item['status']}` | {item['read']} | {metrics} |")

    lines.extend(
        [
            "",
            "## Expected Bridge Pair Checks",
            "",
            "| Pair | Distance | Rank L->R | Rank R->L | Mutual Nearest | Top-2 Both Ways |",
            "| --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for item in report["bridge_pair_checks"]:
        lines.append(
            f"| {item['pair']} | {item.get('distance')} | {item.get('left_rank_of_right')} | "
            f"{item.get('right_rank_of_left')} | {item.get('mutual_nearest')} | {item.get('within_top2_both_directions')} |"
        )

    lines.extend(
        [
            "",
            "## Phase 5 Topographic Bridge",
            "",
            "| Model | Dominant Anchor | Dominant Layer | Archetype | Top-3 Sequence | Overlap Jaccard |",
            "| --- | --- | ---: | --- | --- | ---: |",
        ]
    )
    for item in report["topography_summary"]:
        lines.append(
            f"| {item['model']} | `{item['dominant_anchor']}` | {item['dominant_layer']} | "
            f"{item['path_archetype']} | {item['top3_sequence']} | {item['overlap_jaccard']} |"
        )

    lines.extend(
        [
            "",
            "## Hardware Sign Stability",
            "",
            "| Circuit | Passes | Backends | Mean Parity | Std Parity | Sign Stable | Dominant Mode |",
            "| --- | ---: | --- | ---: | ---: | --- | --- |",
        ]
    )
    for item in report["hardware_summary"]:
        lines.append(
            f"| `{item['circuit']}` | {item['passes']} | {item['backends']} | {item['mean_parity']} | "
            f"{item['std_parity']} | {item['sign_stable']} | `{item['dominant_bitstring_mode']}` |"
        )

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            report["boundary"],
            "",
            "## Next Real Nest 1 Steps",
            "",
            "1. If raw hidden-state vectors are available, rerun `GEO/TOP` on actual point clouds.",
            "2. Build the unified `STAT/PROB/INFO/TENSOR` registry from completed phase packs.",
            "3. Build a real `OPT-1` benchmark instead of treating optimization as mapped-only.",
            "4. Export LSPS transition traces before claiming `CTRL-1` validation.",
            "",
        ]
    )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> dict[str, Any]:
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    report, tables = build_report(args.phase6, args.phase2, args.phase5, args.phase9d, args.residual_root)

    write_csv(out_dir / "nest1_real_trace_feature_matrix.csv", tables["feature_matrix"])
    write_csv(out_dir / "nest1_real_trace_nearest_neighbors.csv", tables["nearest_neighbors"])
    write_csv(out_dir / "nest1_real_trace_topography_bridge.csv", tables["topography_bridge"])
    write_csv(out_dir / "nest1_real_trace_layer_dynamics.csv", tables["layer_dynamics"])
    write_csv(out_dir / "nest1_real_trace_hardware_signs.csv", tables["hardware_signs"])
    (out_dir / "nest1_real_trace_foundation_report.json").write_text(
        json.dumps(json_ready(report), indent=2), encoding="utf-8"
    )
    (out_dir / "nest1_real_trace_foundation_report.md").write_text(render_markdown(report), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase6", type=Path, default=DEFAULT_PHASE6)
    parser.add_argument("--phase2", type=Path, default=DEFAULT_PHASE2)
    parser.add_argument("--phase5", type=Path, default=DEFAULT_PHASE5)
    parser.add_argument("--phase9d", type=Path, default=DEFAULT_PHASE9D)
    parser.add_argument("--residual-root", type=Path, default=DEFAULT_RESIDUAL_ROOT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()
    report = run(args)
    print(json.dumps({"status": report["status"], "out_dir": str(args.out_dir)}, indent=2))


if __name__ == "__main__":
    main()
