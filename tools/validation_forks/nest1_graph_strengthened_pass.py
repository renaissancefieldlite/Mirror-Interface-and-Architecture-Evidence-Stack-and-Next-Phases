#!/usr/bin/env python3
"""Nest 1 GRAPH strengthened pass.

This runner strengthens the earlier GRAPH-lite read without adding toy data.
It uses the real Phase 6 feature artifact and tests graph recovery in two
ways:

- binary kNN edge recovery over the real Phase 6 feature geometry
- weighted/ranked expected-pair recovery over real feature similarity and the
  exported Angle/Amplitude fidelity matrices

The null is exact label permutation over the eight real model labels.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PHASE6 = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase6_pennylane_encoding"
    / "v8_phase6_pennylane_encoding_data_2026-04-22.json"
)
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "nest1_graph_strengthened"

EXPECTED_BRIDGE_PAIRS = [
    ("Mistral", "Hermes"),
    ("Qwen", "DeepSeek"),
    ("GLM", "Nemotron"),
]


def clean_float(value: Any, digits: int = 6) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    return round(numeric, digits)


def load_phase6(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def zscore(matrix: np.ndarray) -> np.ndarray:
    mean = np.mean(matrix, axis=0)
    std = np.std(matrix, axis=0)
    std[std == 0] = 1.0
    return (matrix - mean) / std


def pairwise_distances(matrix: np.ndarray) -> np.ndarray:
    diff = matrix[:, None, :] - matrix[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=2))


def feature_similarity(data: dict[str, Any]) -> tuple[list[str], list[str], np.ndarray]:
    features = list(data["features"])
    labels = [str(model["model"]) for model in data["models"]]
    rows = [
        [float(model["normalized_features"][feature]) for feature in features]
        for model in data["models"]
    ]
    scaled = zscore(np.array(rows, dtype=float))
    distances = pairwise_distances(scaled)
    return labels, features, 1.0 / (1.0 + distances)


def nearest_edges(labels: list[str], similarity: np.ndarray, k: int) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for i, left in enumerate(labels):
        order = [j for j in np.argsort(-similarity[i]) if j != i][:k]
        for j in order:
            edges.add(tuple(sorted((left, labels[j]))))
    return edges


def expected_pair_set() -> set[tuple[str, str]]:
    return {tuple(sorted(pair)) for pair in EXPECTED_BRIDGE_PAIRS}


def expected_edge_hits(edges: set[tuple[str, str]]) -> int:
    return sum(1 for pair in expected_pair_set() if pair in edges)


def binary_knn_sweep(labels: list[str], similarity: np.ndarray) -> list[dict[str, Any]]:
    rows = []
    expected = expected_pair_set()
    for k in range(1, min(5, len(labels))):
        edges = nearest_edges(labels, similarity, k)
        observed_hits = expected_edge_hits(edges)
        null_hits = []
        for perm in itertools.permutations(labels):
            renamed_edges = {
                tuple(sorted((perm[labels.index(left)], perm[labels.index(right)])))
                for left, right in edges
            }
            null_hits.append(expected_edge_hits(renamed_edges))
        p_ge = sum(1 for value in null_hits if value >= observed_hits) / len(null_hits)
        rows.append(
            {
                "view": "feature_similarity",
                "k": k,
                "edge_count": len(edges),
                "expected_pair_edges": f"{observed_hits}/{len(EXPECTED_BRIDGE_PAIRS)}",
                "null_mean_expected_pair_edges": clean_float(np.mean(null_hits)),
                "p_expected_pair_edges_ge_observed": clean_float(p_ge),
                "edges": sorted("/".join(edge) for edge in edges),
            }
        )
    return rows


def score_expected_pairs(label_order: list[str], similarity: np.ndarray) -> dict[str, Any]:
    expected = expected_pair_set()
    all_scores = []
    expected_scores = []
    for i in range(len(label_order)):
        for j in range(i + 1, len(label_order)):
            pair = tuple(sorted((label_order[i], label_order[j])))
            score = float(similarity[i, j])
            all_scores.append((pair, score))
            if pair in expected:
                expected_scores.append(score)

    ranked = sorted(all_scores, key=lambda row: row[1], reverse=True)
    rank_map = {pair: rank + 1 for rank, (pair, _) in enumerate(ranked)}
    expected_ranks = [rank_map[tuple(sorted(pair))] for pair in EXPECTED_BRIDGE_PAIRS]
    return {
        "mean_expected_score": float(np.mean(expected_scores)),
        "mean_all_pair_score": float(np.mean([score for _, score in all_scores])),
        "expected_rank_average": float(np.mean(expected_ranks)),
        "expected_ranks": {
            "/".join(tuple(sorted(pair))): rank
            for pair, rank in zip(EXPECTED_BRIDGE_PAIRS, expected_ranks)
        },
        "top_pairs": [
            {"pair": "/".join(pair), "score": clean_float(score)}
            for pair, score in ranked[:8]
        ],
    }


def ranked_view(label_order: list[str], similarity: np.ndarray, view_name: str) -> dict[str, Any]:
    observed = score_expected_pairs(label_order, similarity)
    null_mean_scores = []
    null_rank_averages = []
    for perm in itertools.permutations(label_order):
        scored = score_expected_pairs(list(perm), similarity)
        null_mean_scores.append(scored["mean_expected_score"])
        null_rank_averages.append(scored["expected_rank_average"])
    mean_ge = sum(
        1 for value in null_mean_scores
        if value >= observed["mean_expected_score"]
    )
    rank_le = sum(
        1 for value in null_rank_averages
        if value <= observed["expected_rank_average"]
    )
    observed_clean = {
        "mean_expected_score": clean_float(observed["mean_expected_score"]),
        "mean_all_pair_score": clean_float(observed["mean_all_pair_score"]),
        "expected_rank_average": clean_float(observed["expected_rank_average"]),
        "expected_ranks": observed["expected_ranks"],
        "top_pairs": observed["top_pairs"],
    }
    return {
        "view": view_name,
        "observed": observed_clean,
        "null": {
            "permutations": len(null_mean_scores),
            "mean_expected_score": clean_float(np.mean(null_mean_scores)),
            "mean_expected_rank_average": clean_float(np.mean(null_rank_averages)),
            "p_mean_expected_score_ge_observed": clean_float(mean_ge / len(null_mean_scores)),
            "p_expected_rank_average_le_observed": clean_float(rank_le / len(null_rank_averages)),
        },
    }


def build_report(phase6_path: Path) -> dict[str, Any]:
    data = load_phase6(phase6_path)
    labels, features, feature_sim = feature_similarity(data)
    angle_sim = np.array(data["angle_fidelity_matrix"], dtype=float)
    amplitude_sim = np.array(data["amplitude_fidelity_matrix"], dtype=float)
    ranked_views = [
        ranked_view(labels, feature_sim, "feature_similarity"),
        ranked_view(labels, angle_sim, "angle_fidelity"),
        ranked_view(labels, amplitude_sim, "amplitude_fidelity"),
    ]
    return {
        "status": "completed_local_strengthened_graph_pass",
        "input": str(phase6_path),
        "features": features,
        "models": labels,
        "expected_bridge_pairs": ["/".join(tuple(sorted(pair))) for pair in EXPECTED_BRIDGE_PAIRS],
        "control": "exact label permutation over real Phase 6 relation matrices",
        "binary_knn_sweep": binary_knn_sweep(labels, feature_sim),
        "ranked_views": ranked_views,
        "read": (
            "The original GRAPH-lite binary kNN edge test was too blunt. The "
            "weighted/ranked Phase 6 feature-similarity graph gives a stronger "
            "expected-pair recovery signal, while Angle/Amplitude fidelity only "
            "strongly recover the Mistral/Hermes pair and do not close the full "
            "GRAPH lane by themselves."
        ),
        "boundary": (
            "This strengthens the AI-side feature graph read. It is not a real "
            "pathway, molecular, allostery, or attention-flow graph validation "
            "until domain-correct graph edges and labels are supplied."
        ),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "nest1_graph_strengthened_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    write_csv(out_dir / "nest1_graph_strengthened_knn_sweep.csv", report["binary_knn_sweep"])

    ranked_rows = []
    for view in report["ranked_views"]:
        ranked_rows.append(
            {
                "view": view["view"],
                **view["observed"],
                **{f"null_{key}": value for key, value in view["null"].items()},
            }
        )
    write_csv(out_dir / "nest1_graph_strengthened_ranked_views.csv", ranked_rows)

    lines = [
        "# Nest 1 GRAPH Strengthened Pass",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Input",
        "",
        f"- Phase 6 artifact: `{report['input']}`",
        f"- Models: `{', '.join(report['models'])}`",
        f"- Expected bridge pairs: `{', '.join(report['expected_bridge_pairs'])}`",
        f"- Control: `{report['control']}`",
        "",
        "## Weighted / Ranked Views",
        "",
        "| View | Mean Expected Score | Mean All-Pair Score | Expected Avg Rank | p(score >= observed) | p(rank <= observed) | Expected Ranks |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for view in report["ranked_views"]:
        obs = view["observed"]
        null = view["null"]
        ranks = ", ".join(f"{pair}: {rank}" for pair, rank in obs["expected_ranks"].items())
        lines.append(
            "| "
            f"`{view['view']}` | "
            f"`{obs['mean_expected_score']}` | "
            f"`{obs['mean_all_pair_score']}` | "
            f"`{obs['expected_rank_average']}` | "
            f"`{null['p_mean_expected_score_ge_observed']}` | "
            f"`{null['p_expected_rank_average_le_observed']}` | "
            f"{ranks} |"
        )
    lines.extend(["", "## Binary kNN Sweep", ""])
    lines.append("| k | Edge Count | Expected Pair Edges | Null Mean | p(edges >= observed) |")
    lines.append("| ---: | ---: | --- | ---: | ---: |")
    for row in report["binary_knn_sweep"]:
        lines.append(
            "| "
            f"`{row['k']}` | "
            f"`{row['edge_count']}` | "
            f"`{row['expected_pair_edges']}` | "
            f"`{row['null_mean_expected_pair_edges']}` | "
            f"`{row['p_expected_pair_edges_ge_observed']}` |"
        )
    lines.extend(["", "## Boundary", "", report["boundary"], ""])
    (out_dir / "nest1_graph_strengthened_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase6", type=Path, default=DEFAULT_PHASE6)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(args.phase6)
    write_report(report, args.out_dir)
    print(f"Wrote GRAPH strengthened report to {args.out_dir}")


if __name__ == "__main__":
    main()
