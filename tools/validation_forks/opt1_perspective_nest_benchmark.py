#!/usr/bin/env python3
"""OPT-1 perspective-nest benchmark.

Runs a real optimization read over existing artifacts:

- V7 condition selection via the locked GAME-1 rubric.
- Phase 6 feature-pair selection against Phase 9D hardware parity similarity.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
GAME1_REPORT = REPO_ROOT / "artifacts" / "validation" / "game1_v7_locked_rubric" / "game1_v7_locked_rubric_report.json"
PHASE6_JSON = REPO_ROOT / "artifacts" / "v8" / "phase6_pennylane_encoding" / "v8_phase6_pennylane_encoding_data_2026-04-22.json"
PHASE9D_JSON = REPO_ROOT / "artifacts" / "v8" / "phase9d_pennylane_remote_repeat" / "v8_phase9d_pennylane_remote_repeat_data_2026-04-22.json"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "opt1_perspective_nest_benchmark"

FEATURES = [
    "peak_percentile",
    "band_width",
    "target_peak",
    "last_peak",
    "phase3_last_to_target",
    "target_to_context",
    "target_to_surround",
    "phase5_last_to_target",
    "anchor_layer_span",
    "overlap_count",
    "overlap_jaccard",
    "dominant_anchor_code",
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_float(value: Any, digits: int = 6) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(numeric):
        return 0.0
    return round(numeric, digits)


def pairwise_similarity(matrix: np.ndarray) -> np.ndarray:
    distances = np.sqrt(np.sum((matrix[:, None, :] - matrix[None, :, :]) ** 2, axis=2))
    return 1.0 / (1.0 + distances)


def zscore(matrix: np.ndarray) -> np.ndarray:
    mean = np.mean(matrix, axis=0)
    std = np.std(matrix, axis=0)
    std[std == 0] = 1.0
    return (matrix - mean) / std


def phase6_similarity(selected: list[str]) -> dict[tuple[str, str], float]:
    data = read_json(PHASE6_JSON)
    by_model = {row["model"]: row for row in data["models"]}
    matrix = np.array(
        [
            [float(by_model[model]["normalized_features"][feature]) for feature in FEATURES]
            for model in selected
        ],
        dtype=float,
    )
    sim = pairwise_similarity(zscore(matrix))
    scores: dict[tuple[str, str], float] = {}
    for left_index, left in enumerate(selected):
        for right_index, right in enumerate(selected):
            if left_index < right_index:
                scores[tuple(sorted((left, right)))] = float(sim[left_index, right_index])
    return scores


def phase9d_hardware_similarity() -> tuple[list[str], dict[tuple[str, str], float]]:
    data = read_json(PHASE9D_JSON)
    parities: dict[str, list[float]] = {}
    for run in data["passes"]:
        for circuit in run.get("circuit_results", []):
            name = str(circuit.get("name", ""))
            if not name.startswith("phase6_feature_"):
                continue
            model = name.removeprefix("phase6_feature_").title()
            parities.setdefault(model, []).append(float(circuit["parity_expectation"]))
    selected = sorted(parities)
    matrix = np.array([parities[model] for model in selected], dtype=float)
    sim = pairwise_similarity(matrix)
    scores: dict[tuple[str, str], float] = {}
    for left_index, left in enumerate(selected):
        for right_index, right in enumerate(selected):
            if left_index < right_index:
                scores[tuple(sorted((left, right)))] = float(sim[left_index, right_index])
    return selected, scores


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(out_dir: Path, report: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "opt1_perspective_nest_benchmark_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# OPT-1 Perspective-Nest Benchmark",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Behavioral Condition Optimization",
        "",
    ]
    for key, value in report["condition_optimization"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Hardware Pair Optimization", ""])
    for key, value in report["hardware_pair_optimization"].items():
        if key != "pair_rows":
            lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "| pair | phase6 feature similarity | hardware parity similarity |", "|---|---:|---:|"])
    for row in report["hardware_pair_optimization"]["pair_rows"]:
        lines.append(f"| `{row['pair']}` | {row['phase6_feature_similarity']} | {row['hardware_parity_similarity']} |")
    lines.extend(["", "## Boundary", "", report["boundary"], "", "## Next Step", "", report["next_step"], ""])
    (out_dir / "opt1_perspective_nest_benchmark_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    out_dir = DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    game = read_json(GAME1_REPORT)
    selected, hardware_scores = phase9d_hardware_similarity()
    feature_scores = phase6_similarity(selected)
    pair_rows = []
    for pair in sorted(hardware_scores):
        pair_rows.append(
            {
                "pair": "/".join(pair),
                "phase6_feature_similarity": clean_float(feature_scores[pair]),
                "hardware_parity_similarity": clean_float(hardware_scores[pair]),
            }
        )
    phase6_best = max(pair_rows, key=lambda row: row["phase6_feature_similarity"])
    hardware_best = max(pair_rows, key=lambda row: row["hardware_parity_similarity"])
    best_pair_agreement = phase6_best["pair"] == hardware_best["pair"]
    condition_supported = game["status"] == "completed_v7_rubric_control_supported"
    hardware_partial = best_pair_agreement and len(pair_rows) == 3
    status = (
        "completed_condition_optimization_supported_hardware_partial"
        if condition_supported and hardware_partial
        else "completed_condition_or_hardware_partial"
    )
    read = (
        "OPT-1 is no longer grammar-only: the V7 perspective condition-selection "
        "objective is control-supported, while the Phase 6 -> Phase 9D hardware "
        "pair-selection objective agrees but remains small-N partial."
        if status == "completed_condition_optimization_supported_hardware_partial"
        else "OPT-1 produced a real benchmark artifact, but the current controls do not close the lane."
    )
    report = {
        "status": status,
        "read": read,
        "condition_optimization": {
            "source": str(GAME1_REPORT.relative_to(REPO_ROOT)),
            "declared_selector": game["metrics"]["declared_mirror_condition"],
            "observed_mean_composite": game["metrics"]["observed_lattice_mean_composite"],
            "shuffle_mean_composite": game["metrics"]["shuffle_mean_composite"],
            "shuffle_p_ge_observed": game["metrics"]["shuffle_p_ge_observed"],
            "status": game["status"],
        },
        "hardware_pair_optimization": {
            "source_phase6": str(PHASE6_JSON.relative_to(REPO_ROOT)),
            "source_phase9d": str(PHASE9D_JSON.relative_to(REPO_ROOT)),
            "hardware_models": ", ".join(selected),
            "pair_rows": pair_rows,
            "phase6_best_pair": phase6_best["pair"],
            "hardware_best_pair": hardware_best["pair"],
            "best_pair_agreement": int(best_pair_agreement),
            "random_pair_baseline_probability": clean_float(1 / len(pair_rows)) if pair_rows else 1.0,
            "status": "small_n_partial" if len(pair_rows) <= 3 else "larger_sample",
        },
        "boundary": (
            "This validates a real optimization benchmark over existing artifacts. "
            "The condition-selection objective is supported; the hardware pair-selection "
            "objective is useful but limited by the three hardware-executed feature circuits."
        ),
        "next_step": (
            "Use this OPT-1 result as condition-optimization support, then expand the "
            "hardware pair objective with more executed feature circuits or move to CAT-1 "
            "composition / transfer scoring."
        ),
    }
    write_csv(out_dir / "opt1_hardware_pair_rows.csv", pair_rows)
    write_report(out_dir, report)
    print(f"Wrote OPT-1 perspective-nest benchmark to {out_dir}")


if __name__ == "__main__":
    main()
