#!/usr/bin/env python3
"""TOP-1/2 closeout for real V8 hidden-state point clouds.

This runner intentionally refuses toy data. If no NPZ point-cloud export is
present, it writes a blocked report instead of generating synthetic topology.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POINT_CLOUD_DIR = ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "point_clouds"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "validation" / "top12_topology_closeout"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TOP-1/2 topology closeout on real point clouds.")
    parser.add_argument("--point-cloud-dir", default=str(DEFAULT_POINT_CLOUD_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument(
        "--tda-mode",
        choices=("h0_mst", "ripser_h1"),
        default="h0_mst",
        help="Topology scorer: H0 MST connectedness or Ripser H1 loop/persistence profile.",
    )
    parser.add_argument("--role", default="target_span_mean", help="Token role to score, or `all`.")
    parser.add_argument("--feature-family", default="all", help="Feature family to score, or `all`.")
    parser.add_argument("--layer-depth", default="all", help="Layer-depth label to score, such as early, middle, late, or `all`.")
    parser.add_argument("--token-region", default="all", help="Token-region label to score, such as pre_anchor, anchor_phrase, post_anchor, or `all`.")
    parser.add_argument(
        "--labels",
        default="lattice,neutral,technical",
        help="Comma-separated labels required for each point cloud.",
    )
    parser.add_argument("--pca-dim", type=int, default=8)
    parser.add_argument("--permutations", type=int, default=1000)
    parser.add_argument(
        "--max-points-per-label",
        type=int,
        default=0,
        help="Deterministically sample up to this many points per label before scoring; 0 keeps all points.",
    )
    parser.add_argument("--seed", type=int, default=67)
    return parser.parse_args()


def standardize(points: np.ndarray) -> np.ndarray:
    centered = points - points.mean(axis=0, keepdims=True)
    scale = centered.std(axis=0, keepdims=True)
    scale[scale == 0.0] = 1.0
    return centered / scale


def pca_reduce(points: np.ndarray, max_dim: int) -> np.ndarray:
    if points.shape[0] < 2:
        return points
    points = standardize(points)
    dim = min(max_dim, points.shape[0] - 1, points.shape[1])
    if dim <= 0 or points.shape[1] <= dim:
        return points
    _, singular_values, vt = np.linalg.svd(points, full_matrices=False)
    return points @ vt[:dim].T


def pairwise_distances(points: np.ndarray) -> np.ndarray:
    diff = points[:, None, :] - points[None, :, :]
    distances = np.sqrt(np.maximum(np.sum(diff * diff, axis=-1), 0.0))
    return distances


def mst_edges(points: np.ndarray) -> np.ndarray:
    n_points = points.shape[0]
    if n_points <= 1:
        return np.array([], dtype=np.float64)
    distances = pairwise_distances(points)
    selected = np.zeros(n_points, dtype=bool)
    selected[0] = True
    edges: list[float] = []
    for _ in range(n_points - 1):
        candidate = np.where(selected[:, None] & ~selected[None, :], distances, np.inf)
        flat_index = int(np.argmin(candidate))
        edge = float(candidate.flat[flat_index])
        if not math.isfinite(edge):
            break
        _, new_index = np.unravel_index(flat_index, candidate.shape)
        selected[new_index] = True
        edges.append(edge)
    return np.array(edges, dtype=np.float64)


def profile(edges: np.ndarray) -> np.ndarray:
    if edges.size == 0:
        return np.zeros(9, dtype=np.float64)
    quantiles = np.quantile(edges, [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
    return np.array(
        [
            float(edges.mean()),
            float(edges.std()),
            *[float(value) for value in quantiles],
        ],
        dtype=np.float64,
    )


def profile_distance(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right))


def h1_persistence_profile(points: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    """Return a compact H1 persistent-homology profile from real points.

    The runner keeps the scoring comparable to the existing H0 closeout:
    each context becomes a fixed-length profile, then context profiles are
    compared against shuffled-label controls. Empty H1 diagrams are valid and
    reported explicitly instead of being inflated into fake structure.
    """

    if points.shape[0] < 4:
        return np.zeros(10, dtype=np.float64), {
            "h1_features": 0,
            "h1_empty": True,
            "reason": "fewer than four points",
        }

    try:
        from ripser import ripser
    except ImportError as exc:  # pragma: no cover - import guard for clean blocked reports
        raise RuntimeError("ripser is required for --tda-mode ripser_h1") from exc

    diagrams = ripser(points, maxdim=1)["dgms"]
    if len(diagrams) < 2:
        diagram = np.empty((0, 2), dtype=np.float64)
    else:
        diagram = np.asarray(diagrams[1], dtype=np.float64)
    finite = diagram[np.isfinite(diagram).all(axis=1)] if diagram.size else np.empty((0, 2), dtype=np.float64)
    if finite.size == 0:
        return np.zeros(10, dtype=np.float64), {
            "h1_features": 0,
            "h1_empty": True,
            "reason": "empty finite H1 diagram",
        }

    persistence = np.maximum(finite[:, 1] - finite[:, 0], 0.0)
    if persistence.size == 0 or float(persistence.max(initial=0.0)) == 0.0:
        return np.zeros(10, dtype=np.float64), {
            "h1_features": int(finite.shape[0]),
            "h1_empty": True,
            "reason": "zero-persistence H1 diagram",
        }

    quantiles = np.quantile(persistence, [0.0, 0.25, 0.5, 0.75, 0.9, 1.0])
    profile_vector = np.array(
        [
            float(finite.shape[0]),
            float(persistence.sum()),
            float(persistence.mean()),
            float(persistence.std()),
            *[float(value) for value in quantiles],
        ],
        dtype=np.float64,
    )
    metadata = {
        "h1_features": int(finite.shape[0]),
        "h1_empty": False,
        "persistence_sum": float(persistence.sum()),
        "persistence_max": float(persistence.max()),
        "birth_min": float(finite[:, 0].min()),
        "death_max": float(finite[:, 1].max()),
    }
    return profile_vector, metadata


def label_list(value: str) -> list[str]:
    labels = [item.strip() for item in value.split(",") if item.strip()]
    if len(labels) < 2:
        raise SystemExit("--labels must include at least two labels.")
    return labels


def topology_score(
    points: np.ndarray,
    labels: np.ndarray,
    contexts: list[str],
    tda_mode: str,
) -> dict[str, Any] | None:
    if not set(contexts).issubset(set(labels.tolist())):
        return None

    profiles: dict[str, np.ndarray] = {}
    profile_metadata: dict[str, dict[str, Any]] = {}
    counts: dict[str, int] = {}
    for context in contexts:
        context_points = points[labels == context]
        counts[context] = int(context_points.shape[0])
        if context_points.shape[0] < 3:
            return None
        if tda_mode == "ripser_h1":
            profiles[context], profile_metadata[context] = h1_persistence_profile(context_points)
        else:
            profiles[context] = profile(mst_edges(context_points))

    pair_distances: dict[str, float] = {}
    for left_index, left in enumerate(contexts):
        for right in contexts[left_index + 1 :]:
            pair_distances[f"{left}__{right}"] = profile_distance(profiles[left], profiles[right])
    strict_score = min(pair_distances.values())

    return {
        "score": strict_score,
        "pair_distances": pair_distances,
        "counts": counts,
        "profile_metadata": profile_metadata,
    }


def sample_per_label(
    points: np.ndarray,
    labels: np.ndarray,
    contexts: list[str],
    max_points_per_label: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    if max_points_per_label <= 0:
        return points, labels
    selected_indices: list[int] = []
    for context in contexts:
        context_indices = np.flatnonzero(labels == context)
        if context_indices.size > max_points_per_label:
            context_indices = np.sort(rng.choice(context_indices, size=max_points_per_label, replace=False))
        selected_indices.extend(int(index) for index in context_indices)
    selected = np.array(sorted(selected_indices), dtype=np.int64)
    return points[selected], labels[selected]


def score_file(path: Path, args: argparse.Namespace, rng: np.random.Generator) -> dict[str, Any]:
    with np.load(path, allow_pickle=False) as payload:
        raw_points = np.asarray(payload["points"])
        finite_mask = np.isfinite(raw_points).all(axis=1)
        points = raw_points[finite_mask].astype(np.float64, copy=False)
        labels = np.asarray(payload["context_label"]).astype(str)
        roles = np.asarray(payload["token_role"]).astype(str)
        if "feature_family" in payload:
            feature_families = np.asarray(payload["feature_family"]).astype(str)
        else:
            feature_families = np.array(["legacy"] * raw_points.shape[0])
        if "layer_depth" in payload:
            layer_depths = np.asarray(payload["layer_depth"]).astype(str)
        else:
            layer_depths = np.array(["legacy"] * raw_points.shape[0])
        if "token_region" in payload:
            token_regions = np.asarray(payload["token_region"]).astype(str)
        else:
            token_regions = np.array(["legacy"] * raw_points.shape[0])
        labels = labels[finite_mask]
        roles = roles[finite_mask]
        feature_families = feature_families[finite_mask]
        layer_depths = layer_depths[finite_mask]
        token_regions = token_regions[finite_mask]

    if args.role != "all":
        role_mask = roles == args.role
        points = points[role_mask]
        labels = labels[role_mask]
        feature_families = feature_families[role_mask]
        layer_depths = layer_depths[role_mask]
        token_regions = token_regions[role_mask]

    if args.feature_family != "all":
        family_mask = feature_families == args.feature_family
        points = points[family_mask]
        labels = labels[family_mask]
        layer_depths = layer_depths[family_mask]
        token_regions = token_regions[family_mask]

    if args.layer_depth != "all":
        depth_mask = layer_depths == args.layer_depth
        points = points[depth_mask]
        labels = labels[depth_mask]
        token_regions = token_regions[depth_mask]

    if args.token_region != "all":
        region_mask = token_regions == args.token_region
        points = points[region_mask]
        labels = labels[region_mask]

    contexts = label_list(args.labels)
    if points.shape[0] == 0:
        return {
            "path": str(path),
            "status": "blocked_empty_point_cloud",
            "reason": "No points remained after role filtering.",
        }

    points, labels = sample_per_label(points, labels, contexts, args.max_points_per_label, rng)
    reduced = pca_reduce(points, args.pca_dim)
    try:
        real = topology_score(reduced, labels, contexts, args.tda_mode)
    except RuntimeError as exc:
        return {
            "path": str(path),
            "status": "blocked_tda_backend_missing",
            "reason": str(exc),
        }
    if real is None:
        return {
            "path": str(path),
            "status": "blocked_insufficient_context_points",
            "reason": f"Need labels {contexts} with at least three points each.",
        }

    null_scores = []
    for _ in range(args.permutations):
        shuffled = labels.copy()
        rng.shuffle(shuffled)
        shuffled_score = topology_score(reduced, shuffled, contexts, args.tda_mode)
        if shuffled_score is not None:
            null_scores.append(float(shuffled_score["score"]))

    if not null_scores:
        return {
            "path": str(path),
            "status": "blocked_null_failed",
            "reason": "No valid shuffled-label null scores were produced.",
            "real": real,
        }

    null = np.array(null_scores, dtype=np.float64)
    separation_p_value = float((np.sum(null >= real["score"]) + 1) / (null.size + 1))
    invariance_p_value = float((np.sum(null <= real["score"]) + 1) / (null.size + 1))
    if separation_p_value <= 0.05:
        status = "topology_separation_supported"
    elif invariance_p_value <= 0.05:
        status = "topology_invariance_supported"
    else:
        status = "not_control_supported"
    return {
        "path": str(path),
        "status": status,
        "tda_mode": args.tda_mode,
        "role": args.role,
        "feature_family": args.feature_family,
        "layer_depth": args.layer_depth,
        "token_region": args.token_region,
        "labels": contexts,
        "max_points_per_label": args.max_points_per_label,
        "points_scored": int(points.shape[0]),
        "pca_dim": args.pca_dim,
        "permutations": int(null.size),
        "separation_p_value": separation_p_value,
        "invariance_p_value": invariance_p_value,
        "real": real,
        "null_mean": float(null.mean()),
        "null_std": float(null.std()),
        "null_p95": float(np.quantile(null, 0.95)),
    }


def build_report(result: dict[str, Any]) -> str:
    lines = [
        "# TOP-1/2 Topology Closeout",
        "",
        f"Date: `{result['generated_at']}`",
        "",
        "## Purpose",
        "",
        "This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.",
        "",
        "## Status",
        "",
        f"- overall status: `{result['status']}`",
        f"- point-cloud directory: `{result['point_cloud_dir']}`",
        f"- TDA backend: `{result['tda_backend']}`",
        f"- TDA mode: `{result['tda_mode']}`",
        f"- role: `{result['role']}`",
        f"- feature family: `{result['feature_family']}`",
        f"- layer depth: `{result['layer_depth']}`",
        f"- token region: `{result['token_region']}`",
        f"- labels: `{', '.join(result['labels'])}`",
        f"- max points per label: `{result['max_points_per_label']}`",
        f"- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels",
        "",
    ]
    if result["status"] == "blocked_missing_point_clouds":
        lines.extend(
            [
                "## Blocker",
                "",
                "No `.npz` point clouds were found. This is the correct blocked result until the V8 runner exports raw hidden-state vectors.",
                "",
                "Required export:",
                "",
                "```bash",
                "python3 /Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/run_v8_residual_stream_probe.py --export-point-clouds",
                "```",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "## Model Results",
            "",
            "| Point Cloud | Status | Points | Separation p | Invariance p | Real Score | Null Mean |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in result["models"]:
        real_score = item.get("real", {}).get("score", "n/a")
        lines.append(
            "| "
            f"`{Path(item['path']).name}` | "
            f"`{item['status']}` | "
            f"`{item.get('points_scored', 'n/a')}` | "
            f"`{item.get('separation_p_value', 'n/a')}` | "
            f"`{item.get('invariance_p_value', 'n/a')}` | "
            f"`{real_score}` | "
            f"`{item.get('null_mean', 'n/a')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This closeout uses real exported V8 hidden-state point clouds only. `h0_mst` reads connectedness; `ripser_h1` reads loop / persistence profiles. Separation and invariance are both tested against shuffled-label controls.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    point_cloud_dir = Path(args.point_cloud_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    point_clouds = sorted(point_cloud_dir.glob("*.npz"))
    tda_backend = "ripser_available" if importlib.util.find_spec("ripser") else "h0_mst_only"
    result: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(),
        "point_cloud_dir": str(point_cloud_dir),
        "output_dir": str(output_dir),
        "role": args.role,
        "feature_family": args.feature_family,
        "layer_depth": args.layer_depth,
        "token_region": args.token_region,
        "tda_mode": args.tda_mode,
        "labels": label_list(args.labels),
        "max_points_per_label": args.max_points_per_label,
        "pca_dim": args.pca_dim,
        "tda_backend": tda_backend,
        "models": [],
    }

    if not point_clouds:
        result["status"] = "blocked_missing_point_clouds"
    else:
        result["models"] = [score_file(path, args, rng) for path in point_clouds]
        supported_statuses = {"topology_separation_supported", "topology_invariance_supported"}
        supported = sum(1 for item in result["models"] if item.get("status") in supported_statuses)
        result["supported_models"] = supported
        result["tested_models"] = len(result["models"])
        if supported == len(result["models"]):
            result["status"] = "control_supported"
        elif supported > 0:
            result["status"] = "mixed_partial_support"
        else:
            result["status"] = "not_control_supported_or_blocked"

    json_path = output_dir / "top12_topology_closeout.json"
    md_path = output_dir / "top12_topology_closeout_report.md"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(build_report(result), encoding="utf-8")
    print(json.dumps({"status": result["status"], "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
