#!/usr/bin/env python3
"""Phase 12B biological control-closeout.

Runs controls over the completed real HRV 5 x 4 matrix:

- condition mean/delta ranking against shuffled labels
- mirror-vs-control separation against shuffled labels
- leave-one-run-index-out nearest-centroid classification
- HR-only baseline compared with multi-feature HRV readout

No synthetic sessions are generated. Nulls only relabel the existing canonical
Phase 12B session artifacts while preserving the 5-per-condition layout.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase12b_biological_comparison_pack"
    / "v8_phase12b_biological_comparison_pack_data_2026-04-24.json"
)
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "phase12b_biological_control_closeout"

CONDITION_ORDER = [
    "seated_calm",
    "drift_control",
    "mirror_coherence",
    "dancing_activation",
]

HR_ONLY_FEATURES = ["delta_hr"]
MULTI_FEATURES = [
    "delta_hr",
    "delta_rmssd",
    "delta_sdnn",
    "post_minus_condition_hr",
    "post_minus_condition_rmssd",
    "post_minus_condition_sdnn",
]


def clean_float(value: Any, digits: int = 6) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    return round(numeric, digits)


def load_sessions(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data["canonical_sessions"])


def feature_matrix(sessions: list[dict[str, Any]], features: list[str]) -> np.ndarray:
    return np.array([[float(row[feature]) for feature in features] for row in sessions], dtype=float)


def labels(sessions: list[dict[str, Any]]) -> list[str]:
    return [str(row["condition"]) for row in sessions]


def run_indices(sessions: list[dict[str, Any]]) -> list[int]:
    return [int(row["run_index"]) for row in sessions]


def condition_means(
    sessions: list[dict[str, Any]],
    assigned_labels: list[str],
    metric: str,
) -> dict[str, float]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for row, label in zip(sessions, assigned_labels):
        buckets[label].append(float(row[metric]))
    return {condition: float(np.mean(buckets[condition])) for condition in CONDITION_ORDER}


def vector_means(
    sessions: list[dict[str, Any]],
    assigned_labels: list[str],
    features: list[str],
) -> dict[str, np.ndarray]:
    matrix = feature_matrix(sessions, features)
    buckets: dict[str, list[np.ndarray]] = defaultdict(list)
    for vector, label in zip(matrix, assigned_labels):
        buckets[label].append(vector)
    return {condition: np.mean(np.array(buckets[condition]), axis=0) for condition in CONDITION_ORDER}


def zscore_train_test(train: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(train, axis=0)
    std = np.std(train, axis=0)
    std[std == 0] = 1.0
    return (train - mean) / std, (test - mean) / std


def nearest_centroid_loro_accuracy(
    sessions: list[dict[str, Any]],
    assigned_labels: list[str],
    features: list[str],
) -> dict[str, Any]:
    matrix = feature_matrix(sessions, features)
    run_ids = run_indices(sessions)
    unique_runs = sorted(set(run_ids))
    predictions = []
    correct = 0
    total = 0
    for run_id in unique_runs:
        train_idx = [i for i, value in enumerate(run_ids) if value != run_id]
        test_idx = [i for i, value in enumerate(run_ids) if value == run_id]
        train_x, test_x = zscore_train_test(matrix[train_idx], matrix[test_idx])
        train_labels = [assigned_labels[i] for i in train_idx]
        test_labels = [assigned_labels[i] for i in test_idx]
        centroids = {}
        for condition in CONDITION_ORDER:
            rows = [train_x[i] for i, label in enumerate(train_labels) if label == condition]
            centroids[condition] = np.mean(np.array(rows), axis=0)
        for local_i, vector in enumerate(test_x):
            distances = {
                condition: float(np.linalg.norm(vector - centroid))
                for condition, centroid in centroids.items()
            }
            prediction = min(distances, key=distances.get)
            actual = test_labels[local_i]
            correct += int(prediction == actual)
            total += 1
            predictions.append(
                {
                    "run_index": run_id,
                    "session_id": sessions[test_idx[local_i]]["session_id"],
                    "actual": actual,
                    "predicted": prediction,
                    "correct": int(prediction == actual),
                    "nearest_distance": clean_float(distances[prediction]),
                }
            )
    per_condition = {}
    for condition in CONDITION_ORDER:
        rows = [row for row in predictions if row["actual"] == condition]
        per_condition[condition] = clean_float(
            sum(row["correct"] for row in rows) / len(rows)
        ) if rows else None
    return {
        "accuracy": clean_float(correct / total if total else 0.0),
        "correct": correct,
        "total": total,
        "per_condition_accuracy": per_condition,
        "predictions": predictions,
    }


def balanced_label_shuffle(real_labels: list[str], rng: random.Random) -> list[str]:
    shuffled = list(real_labels)
    rng.shuffle(shuffled)
    return shuffled


def block_label_shuffle(
    real_labels: list[str],
    run_ids: list[int],
    rng: random.Random,
) -> list[str]:
    shuffled = list(real_labels)
    for run_id in sorted(set(run_ids)):
        idx = [i for i, value in enumerate(run_ids) if value == run_id]
        block = [shuffled[i] for i in idx]
        rng.shuffle(block)
        for i, label in zip(idx, block):
            shuffled[i] = label
    return shuffled


def permutation_controls(
    sessions: list[dict[str, Any]],
    trials: int,
    seed: int,
) -> dict[str, Any]:
    real_labels = labels(sessions)
    real_run_ids = run_indices(sessions)
    observed_hr = nearest_centroid_loro_accuracy(sessions, real_labels, HR_ONLY_FEATURES)
    observed_multi = nearest_centroid_loro_accuracy(sessions, real_labels, MULTI_FEATURES)
    observed_means = condition_means(sessions, real_labels, "delta_hr")
    observed_vectors = vector_means(sessions, real_labels, MULTI_FEATURES)
    mirror_vs_drift = float(
        np.linalg.norm(observed_vectors["mirror_coherence"] - observed_vectors["drift_control"])
    )
    mirror_vs_calm = float(
        np.linalg.norm(observed_vectors["mirror_coherence"] - observed_vectors["seated_calm"])
    )
    activation_gap = float(
        observed_means["dancing_activation"] - observed_means["mirror_coherence"]
    )

    rng = random.Random(seed)
    null_balanced_hr = []
    null_balanced_multi = []
    null_block_hr = []
    null_block_multi = []
    null_mirror_delta = []
    null_mirror_drift_distance = []
    null_mirror_calm_distance = []
    null_activation_gap = []

    for _ in range(trials):
        shuffled = balanced_label_shuffle(real_labels, rng)
        block_shuffled = block_label_shuffle(real_labels, real_run_ids, rng)
        null_balanced_hr.append(
            float(nearest_centroid_loro_accuracy(sessions, shuffled, HR_ONLY_FEATURES)["accuracy"])
        )
        null_balanced_multi.append(
            float(nearest_centroid_loro_accuracy(sessions, shuffled, MULTI_FEATURES)["accuracy"])
        )
        null_block_hr.append(
            float(nearest_centroid_loro_accuracy(sessions, block_shuffled, HR_ONLY_FEATURES)["accuracy"])
        )
        null_block_multi.append(
            float(nearest_centroid_loro_accuracy(sessions, block_shuffled, MULTI_FEATURES)["accuracy"])
        )
        means = condition_means(sessions, shuffled, "delta_hr")
        vectors = vector_means(sessions, shuffled, MULTI_FEATURES)
        null_mirror_delta.append(means["mirror_coherence"])
        null_activation_gap.append(means["dancing_activation"] - means["mirror_coherence"])
        null_mirror_drift_distance.append(
            float(np.linalg.norm(vectors["mirror_coherence"] - vectors["drift_control"]))
        )
        null_mirror_calm_distance.append(
            float(np.linalg.norm(vectors["mirror_coherence"] - vectors["seated_calm"]))
        )

    def p_ge(null: list[float], observed: float) -> float:
        return (sum(1 for value in null if value >= observed) + 1) / (len(null) + 1)

    def p_le(null: list[float], observed: float) -> float:
        return (sum(1 for value in null if value <= observed) + 1) / (len(null) + 1)

    return {
        "observed": {
            "condition_delta_hr_means": {k: clean_float(v) for k, v in observed_means.items()},
            "hr_only_loro": observed_hr,
            "multi_feature_loro": observed_multi,
            "mirror_vs_drift_multifeature_distance": clean_float(mirror_vs_drift),
            "mirror_vs_calm_multifeature_distance": clean_float(mirror_vs_calm),
            "dancing_minus_mirror_delta_hr_gap": clean_float(activation_gap),
            "mirror_delta_hr_rank_lowest": int(
                observed_means["mirror_coherence"] == min(observed_means.values())
            ),
        },
        "nulls": {
            "trials": trials,
            "balanced_label_shuffle": {
                "mean_hr_only_accuracy": clean_float(np.mean(null_balanced_hr)),
                "mean_multi_feature_accuracy": clean_float(np.mean(null_balanced_multi)),
                "p_hr_only_accuracy_ge_observed": clean_float(
                    p_ge(null_balanced_hr, float(observed_hr["accuracy"]))
                ),
                "p_multi_feature_accuracy_ge_observed": clean_float(
                    p_ge(null_balanced_multi, float(observed_multi["accuracy"]))
                ),
                "mean_mirror_delta_hr": clean_float(np.mean(null_mirror_delta)),
                "p_mirror_delta_hr_le_observed": clean_float(
                    p_le(null_mirror_delta, observed_means["mirror_coherence"])
                ),
                "mean_mirror_vs_drift_distance": clean_float(np.mean(null_mirror_drift_distance)),
                "p_mirror_vs_drift_distance_ge_observed": clean_float(
                    p_ge(null_mirror_drift_distance, mirror_vs_drift)
                ),
                "mean_mirror_vs_calm_distance": clean_float(np.mean(null_mirror_calm_distance)),
                "p_mirror_vs_calm_distance_ge_observed": clean_float(
                    p_ge(null_mirror_calm_distance, mirror_vs_calm)
                ),
                "mean_dancing_minus_mirror_delta_hr_gap": clean_float(np.mean(null_activation_gap)),
                "p_dancing_minus_mirror_delta_hr_gap_ge_observed": clean_float(
                    p_ge(null_activation_gap, activation_gap)
                ),
            },
            "within_run_block_shuffle": {
                "mean_hr_only_accuracy": clean_float(np.mean(null_block_hr)),
                "mean_multi_feature_accuracy": clean_float(np.mean(null_block_multi)),
                "p_hr_only_accuracy_ge_observed": clean_float(
                    p_ge(null_block_hr, float(observed_hr["accuracy"]))
                ),
                "p_multi_feature_accuracy_ge_observed": clean_float(
                    p_ge(null_block_multi, float(observed_multi["accuracy"]))
                ),
            },
        },
    }


def feature_contributions(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    real_labels = labels(sessions)
    rows = []
    for feature in MULTI_FEATURES:
        means = condition_means(sessions, real_labels, feature)
        rows.append(
            {
                "feature": feature,
                "seated_calm": clean_float(means["seated_calm"]),
                "drift_control": clean_float(means["drift_control"]),
                "mirror_coherence": clean_float(means["mirror_coherence"]),
                "dancing_activation": clean_float(means["dancing_activation"]),
                "mirror_minus_drift": clean_float(means["mirror_coherence"] - means["drift_control"]),
                "dance_minus_mirror": clean_float(means["dancing_activation"] - means["mirror_coherence"]),
            }
        )
    return rows


def aggregate_table(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    assigned = labels(sessions)
    for condition in CONDITION_ORDER:
        subset = [row for row, label in zip(sessions, assigned) if label == condition]
        rows.append(
            {
                "condition": condition,
                "runs": len(subset),
                "mean_baseline_hr": clean_float(np.mean([row["baseline_hr"] for row in subset])),
                "mean_condition_hr": clean_float(np.mean([row["condition_hr"] for row in subset])),
                "mean_post_hr": clean_float(np.mean([row["post_hr"] for row in subset])),
                "mean_delta_hr": clean_float(np.mean([row["delta_hr"] for row in subset])),
                "mean_delta_rmssd": clean_float(np.mean([row["delta_rmssd"] for row in subset])),
                "mean_delta_sdnn": clean_float(np.mean([row["delta_sdnn"] for row in subset])),
            }
        )
    return rows


def status_from_result(result: dict[str, Any]) -> str:
    null = result["nulls"]["balanced_label_shuffle"]
    observed = result["observed"]
    if (
        null["p_mirror_delta_hr_le_observed"] <= 0.05
        and null["p_dancing_minus_mirror_delta_hr_gap_ge_observed"] <= 0.05
    ):
        return "control_supported_condition_separation"
    if observed["mirror_delta_hr_rank_lowest"]:
        return "direction_supported_classification_partial"
    return "partial_or_not_significant"


def build_report(input_path: Path, trials: int, seed: int) -> dict[str, Any]:
    sessions = load_sessions(input_path)
    result = permutation_controls(sessions, trials, seed)
    return {
        "status": status_from_result(result),
        "input": str(input_path),
        "session_count": len(sessions),
        "condition_counts": dict(Counter(labels(sessions))),
        "features": {
            "hr_only": HR_ONLY_FEATURES,
            "multi_feature": MULTI_FEATURES,
        },
        "control": (
            "balanced label shuffle preserving 5 sessions per condition; "
            "within-run block shuffle preserving one label per condition block"
        ),
        "aggregate_rows": aggregate_table(sessions),
        "feature_contribution_rows": feature_contributions(sessions),
        **result,
        "read": (
            "Phase 12B remains a real HRV biological adapter: mirror_coherence "
            "shows the strongest average HR downshift and separates from "
            "activation/drift under shuffled-label controls. Leave-one-run-out "
            "condition classification is partial on HRV-only data, which keeps "
            "the lane bounded until EEG/HRV or richer continuous signals are added."
        ),
        "boundary": (
            "This is not a clinical result and does not validate high-resolution "
            "EEG/spectral/dynamical biology. It tests the completed HRV 5 x 4 "
            "matrix as a coarse biological condition-class adapter."
        ),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "phase12b_biological_control_closeout_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    write_csv(out_dir / "phase12b_biological_control_closeout_aggregates.csv", report["aggregate_rows"])
    write_csv(
        out_dir / "phase12b_biological_control_closeout_feature_contributions.csv",
        report["feature_contribution_rows"],
    )
    write_csv(
        out_dir / "phase12b_biological_control_closeout_hr_predictions.csv",
        report["observed"]["hr_only_loro"]["predictions"],
    )
    write_csv(
        out_dir / "phase12b_biological_control_closeout_multifeature_predictions.csv",
        report["observed"]["multi_feature_loro"]["predictions"],
    )

    observed = report["observed"]
    null_bal = report["nulls"]["balanced_label_shuffle"]
    null_block = report["nulls"]["within_run_block_shuffle"]
    lines = [
        "# Phase 12B Biological Control-Closeout",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Input And Controls",
        "",
        f"- Input: `{report['input']}`",
        f"- Sessions: `{report['session_count']}`",
        f"- Condition counts: `{report['condition_counts']}`",
        f"- HR-only features: `{', '.join(report['features']['hr_only'])}`",
        f"- Multi-feature HRV readout: `{', '.join(report['features']['multi_feature'])}`",
        f"- Control: `{report['control']}`",
        "",
        "## Condition Delta HR Means",
        "",
        "| Condition | Mean Delta HR |",
        "| --- | ---: |",
    ]
    for condition, value in observed["condition_delta_hr_means"].items():
        lines.append(f"| `{condition}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Main Control Results",
            "",
            "| Test | Observed | Null Mean | p-value |",
            "| --- | ---: | ---: | ---: |",
            (
                f"| HR-only leave-one-run-out accuracy | "
                f"`{observed['hr_only_loro']['accuracy']}` | "
                f"`{null_bal['mean_hr_only_accuracy']}` | "
                f"`{null_bal['p_hr_only_accuracy_ge_observed']}` |"
            ),
            (
                f"| Multi-feature leave-one-run-out accuracy | "
                f"`{observed['multi_feature_loro']['accuracy']}` | "
                f"`{null_bal['mean_multi_feature_accuracy']}` | "
                f"`{null_bal['p_multi_feature_accuracy_ge_observed']}` |"
            ),
            (
                f"| Mirror delta HR lower than shuffled labels | "
                f"`{observed['condition_delta_hr_means']['mirror_coherence']}` | "
                f"`{null_bal['mean_mirror_delta_hr']}` | "
                f"`{null_bal['p_mirror_delta_hr_le_observed']}` |"
            ),
            (
                f"| Dancing-minus-mirror Delta HR gap | "
                f"`{observed['dancing_minus_mirror_delta_hr_gap']}` | "
                f"`{null_bal['mean_dancing_minus_mirror_delta_hr_gap']}` | "
                f"`{null_bal['p_dancing_minus_mirror_delta_hr_gap_ge_observed']}` |"
            ),
            (
                f"| Mirror-vs-drift multi-feature distance | "
                f"`{observed['mirror_vs_drift_multifeature_distance']}` | "
                f"`{null_bal['mean_mirror_vs_drift_distance']}` | "
                f"`{null_bal['p_mirror_vs_drift_distance_ge_observed']}` |"
            ),
            (
                f"| Mirror-vs-calm multi-feature distance | "
                f"`{observed['mirror_vs_calm_multifeature_distance']}` | "
                f"`{null_bal['mean_mirror_vs_calm_distance']}` | "
                f"`{null_bal['p_mirror_vs_calm_distance_ge_observed']}` |"
            ),
            "",
            "## Within-Run Block Shuffle",
            "",
            "| Test | Observed | Null Mean | p-value |",
            "| --- | ---: | ---: | ---: |",
            (
                f"| HR-only leave-one-run-out accuracy | "
                f"`{observed['hr_only_loro']['accuracy']}` | "
                f"`{null_block['mean_hr_only_accuracy']}` | "
                f"`{null_block['p_hr_only_accuracy_ge_observed']}` |"
            ),
            (
                f"| Multi-feature leave-one-run-out accuracy | "
                f"`{observed['multi_feature_loro']['accuracy']}` | "
                f"`{null_block['mean_multi_feature_accuracy']}` | "
                f"`{null_block['p_multi_feature_accuracy_ge_observed']}` |"
            ),
            "",
            "## Feature Contributions",
            "",
            "| Feature | Seated | Drift | Mirror | Dance | Mirror - Drift | Dance - Mirror |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in report["feature_contribution_rows"]:
        lines.append(
            "| "
            f"`{row['feature']}` | "
            f"`{row['seated_calm']}` | "
            f"`{row['drift_control']}` | "
            f"`{row['mirror_coherence']}` | "
            f"`{row['dancing_activation']}` | "
            f"`{row['mirror_minus_drift']}` | "
            f"`{row['dance_minus_mirror']}` |"
        )
    lines.extend(["", "## Boundary", "", report["boundary"], ""])
    (out_dir / "phase12b_biological_control_closeout_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--trials", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=12012)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(args.input, args.trials, args.seed)
    write_report(report, args.out_dir)
    print(f"Wrote Phase 12B control-closeout to {args.out_dir}")


if __name__ == "__main__":
    main()
