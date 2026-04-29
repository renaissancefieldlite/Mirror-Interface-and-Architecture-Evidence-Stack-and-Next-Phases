#!/usr/bin/env python3
"""DE-1 -> Phase 12B HRV dynamics validation fork.

This runner keeps the Nest 1 standard grounded in real measurements. It reads
the actual Phase 12B MoFit RR/BPM session exports and tests whether a bounded
differential-equation style lens can separate condition classes above a simple
heart-rate delta baseline.

No synthetic rows are generated here. Missing real files produce a blocked report.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
PLAYGROUND_ROOT = REPO_ROOT.parents[0]
DEFAULT_PHASE12B = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase12b_biological_comparison_pack"
    / "v8_phase12b_biological_comparison_pack_data_2026-04-24.json"
)
DEFAULT_HRV_ROOT = PLAYGROUND_ROOT / "renaissancefieldlitehrv1.0" / "data" / "field_sessions"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "de1_hrv_dynamics"

HR_ONLY_COLUMNS = ["delta_bpm_mean"]
DE1_BPM_COLUMNS = [
    "delta_bpm_a",
    "delta_bpm_b",
    "delta_bpm_rmse",
    "delta_bpm_r2",
    "delta_bpm_mean_abs_dx",
    "delta_bpm_dx_std",
    "delta_bpm_zero_crossing_rate",
]
DE1_RR_COLUMNS = [
    "delta_rr_ms_a",
    "delta_rr_ms_b",
    "delta_rr_ms_rmse",
    "delta_rr_ms_r2",
    "delta_rr_ms_mean_abs_dx",
    "delta_rr_ms_dx_std",
    "delta_rr_ms_zero_crossing_rate",
]
DE1_COMPOSITE_COLUMNS = DE1_BPM_COLUMNS + DE1_RR_COLUMNS
DE1_WITH_MEAN_COLUMNS = DE1_COMPOSITE_COLUMNS + ["delta_bpm_mean", "delta_rr_ms_mean"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_samples(path: Path) -> list[dict[str, float]]:
    rows = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                seconds = float(row["relative_seconds"])
                rr_ms = float(row["rr_ms"])
                bpm = float(row["bpm"])
            except (KeyError, TypeError, ValueError):
                continue
            if 250 <= rr_ms <= 2000 and 30 <= bpm <= 240:
                rows.append({"relative_seconds": seconds, "rr_ms": rr_ms, "bpm": bpm})
    return rows


def session_windows(session_meta: dict) -> dict[str, tuple[float, float]]:
    baseline_duration = float(session_meta["windows"]["baseline"]["duration_seconds"])
    condition_duration = float(session_meta["windows"]["condition"]["duration_seconds"])
    post_duration = float(session_meta["windows"]["post"]["duration_seconds"])
    baseline = (0.0, baseline_duration)
    condition = (baseline[1], baseline[1] + condition_duration)
    post = (condition[1], condition[1] + post_duration)
    return {"baseline": baseline, "condition": condition, "post": post}


def interpolate_window(
    samples: list[dict[str, float]],
    start: float,
    end: float,
    key: str,
    sample_rate_hz: float = 1.0,
) -> np.ndarray | None:
    rows = [row for row in samples if start <= row["relative_seconds"] < end]
    if len(rows) < 12:
        return None
    times = np.array([row["relative_seconds"] for row in rows], dtype=float)
    values = np.array([row[key] for row in rows], dtype=float)
    if len(np.unique(times)) < 4:
        return None
    grid = np.arange(start, end, 1.0 / sample_rate_hz, dtype=float)
    if len(grid) < 12:
        return None
    return np.interp(grid, times, values)


def zero_crossing_rate(values: np.ndarray) -> float:
    if len(values) < 3:
        return 0.0
    signs = np.sign(values)
    signs[signs == 0] = 1
    return float(np.mean(signs[1:] != signs[:-1]))


def fit_first_order_dynamics(values: np.ndarray) -> dict[str, float] | None:
    """Fit dx = a * (x - mean(x)) + b on a 1Hz interpolated signal."""
    if len(values) < 12:
        return None
    x = values[:-1]
    dx = np.diff(values)
    if len(dx) < 8:
        return None

    x_centered = x - float(np.mean(x))
    design = np.column_stack([x_centered, np.ones_like(x_centered)])
    try:
        coef = np.linalg.lstsq(design, dx, rcond=None)[0]
    except np.linalg.LinAlgError:
        return None

    prediction = design @ coef
    residual = dx - prediction
    ss_res = float(np.sum(residual * residual))
    ss_tot = float(np.sum((dx - float(np.mean(dx))) ** 2))
    return {
        "a": float(coef[0]),
        "b": float(coef[1]),
        "rmse": float(np.sqrt(np.mean(residual * residual))),
        "r2": float(1.0 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0,
        "mean_abs_dx": float(np.mean(np.abs(dx))),
        "dx_std": float(np.std(dx, ddof=1)) if len(dx) > 1 else 0.0,
        "zero_crossing_rate": zero_crossing_rate(dx),
        "mean": float(np.mean(values)),
        "std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
        "range": float(np.max(values) - np.min(values)),
        "n": int(len(values)),
    }


def signal_window_features(
    samples: list[dict[str, float]],
    start: float,
    end: float,
    signal_key: str,
) -> dict[str, float] | None:
    values = interpolate_window(samples, start, end, signal_key)
    if values is None:
        return None
    return fit_first_order_dynamics(values)


def safe_delta(condition: dict[str, float], baseline: dict[str, float], key: str) -> float:
    left = condition.get(key, float("nan"))
    right = baseline.get(key, float("nan"))
    if math.isnan(left) or math.isnan(right):
        return float("nan")
    return left - right


def add_signal_features(
    row: dict[str, object],
    prefix: str,
    baseline: dict[str, float],
    condition: dict[str, float],
    post: dict[str, float],
) -> None:
    keys = ["a", "b", "rmse", "r2", "mean_abs_dx", "dx_std", "zero_crossing_rate", "mean", "std", "range", "n"]
    for key in keys:
        row[f"baseline_{prefix}_{key}"] = baseline[key]
        row[f"condition_{prefix}_{key}"] = condition[key]
        row[f"post_{prefix}_{key}"] = post[key]
        row[f"delta_{prefix}_{key}"] = safe_delta(condition, baseline, key)
        row[f"post_delta_{prefix}_{key}"] = safe_delta(post, condition, key)


def build_feature_rows(phase12b_path: Path, hrv_root: Path) -> tuple[list[dict[str, object]], list[str]]:
    phase12b = load_json(phase12b_path)
    rows: list[dict[str, object]] = []
    blocked: list[str] = []

    for session in phase12b.get("canonical_sessions", []):
        session_id = session["session_id"]
        session_dir = hrv_root / session_id
        sample_path = session_dir / f"{session_id}_samples.csv"
        meta_path = session_dir / f"{session_id}.json"
        if not sample_path.exists() or not meta_path.exists():
            blocked.append(f"{session_id}: missing metadata or sample CSV")
            continue

        samples = load_samples(sample_path)
        if len(samples) < 36:
            blocked.append(f"{session_id}: insufficient valid samples")
            continue

        windows = session_windows(load_json(meta_path))
        feature_bundle: dict[str, dict[str, dict[str, float]]] = {"bpm": {}, "rr_ms": {}}
        valid = True
        for signal_key in ("bpm", "rr_ms"):
            for window_label, (start, end) in windows.items():
                features = signal_window_features(samples, start, end, signal_key)
                if features is None:
                    blocked.append(f"{session_id}: unable to fit {signal_key} {window_label} window")
                    valid = False
                    break
                feature_bundle[signal_key][window_label] = features
            if not valid:
                break
        if not valid:
            continue

        row: dict[str, object] = {
            "condition": session["condition"],
            "run_label": session["run_label"],
            "run_index": session["run_index"],
            "session_id": session_id,
        }
        add_signal_features(
            row,
            "bpm",
            feature_bundle["bpm"]["baseline"],
            feature_bundle["bpm"]["condition"],
            feature_bundle["bpm"]["post"],
        )
        add_signal_features(
            row,
            "rr_ms",
            feature_bundle["rr_ms"]["baseline"],
            feature_bundle["rr_ms"]["condition"],
            feature_bundle["rr_ms"]["post"],
        )
        rows.append(row)
    return rows, blocked


def matrix(rows: list[dict[str, object]], columns: list[str]) -> np.ndarray:
    values = []
    for row in rows:
        values.append([float(row[column]) for column in columns])
    arr = np.array(values, dtype=float)
    col_mean = np.nanmean(arr, axis=0)
    inds = np.where(np.isnan(arr))
    arr[inds] = np.take(col_mean, inds[1])
    col_std = np.std(arr, axis=0)
    col_std[col_std == 0] = 1.0
    return (arr - np.mean(arr, axis=0)) / col_std


def leave_one_out_centroid(rows: list[dict[str, object]], columns: list[str]) -> dict:
    if len(rows) < 2:
        return {"accuracy": 0.0, "correct": 0, "total": len(rows), "predictions": [], "confusion": {}}

    labels = [str(row["condition"]) for row in rows]
    x = matrix(rows, columns)
    predictions = []
    correct = 0
    for index, label in enumerate(labels):
        train_indices = [i for i in range(len(rows)) if i != index]
        centroids = {}
        for train_label in sorted(set(labels)):
            class_indices = [i for i in train_indices if labels[i] == train_label]
            if class_indices:
                centroids[train_label] = np.mean(x[class_indices], axis=0)
        distances = {
            train_label: float(np.linalg.norm(x[index] - centroid))
            for train_label, centroid in centroids.items()
        }
        predicted = min(distances, key=distances.get)
        if predicted == label:
            correct += 1
        predictions.append(
            {
                "run_label": rows[index]["run_label"],
                "actual": label,
                "predicted": predicted,
                "correct": predicted == label,
                "nearest_distances": distances,
            }
        )

    confusion: dict[str, dict[str, int]] = {}
    for item in predictions:
        actual = str(item["actual"])
        predicted = str(item["predicted"])
        confusion.setdefault(actual, {})
        confusion[actual][predicted] = confusion[actual].get(predicted, 0) + 1

    return {
        "accuracy": round(correct / len(rows), 3),
        "correct": correct,
        "total": len(rows),
        "predictions": predictions,
        "confusion": confusion,
    }


def condition_summary(rows: list[dict[str, object]], columns: Iterable[str]) -> dict[str, dict[str, float]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["condition"])].append(row)
    summary: dict[str, dict[str, float]] = {}
    for condition, condition_rows in grouped.items():
        summary[condition] = {"runs": len(condition_rows)}
        for column in columns:
            values = [float(row[column]) for row in condition_rows]
            summary[condition][f"mean_{column}"] = round(float(np.mean(values)), 6)
    return summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def blocked_report(phase12b_path: Path, hrv_root: Path, out_dir: Path, reasons: list[str]) -> dict:
    report = {
        "status": "blocked",
        "validation_fork": "Nest 1 DE-1 -> Phase 12B HRV dynamics",
        "inputs": {"phase12b_path": str(phase12b_path), "hrv_root": str(hrv_root)},
        "blocked_reasons": reasons,
        "boundary": "No synthetic data generated. This fork requires real HRV session files.",
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "de1_hrv_dynamics_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (out_dir / "de1_hrv_dynamics_report.md").write_text(render_markdown(report), encoding="utf-8")
    return report


def build_report(rows: list[dict[str, object]], blocked: list[str], phase12b_path: Path, hrv_root: Path) -> dict:
    validations = {
        "hr_only": {
            **leave_one_out_centroid(rows, HR_ONLY_COLUMNS),
            "columns": HR_ONLY_COLUMNS,
            "read": "naive mean-BPM delta baseline",
        },
        "de1_bpm_dynamics": {
            **leave_one_out_centroid(rows, DE1_BPM_COLUMNS),
            "columns": DE1_BPM_COLUMNS,
            "read": "DE-1 local dynamics over BPM only",
        },
        "de1_rr_dynamics": {
            **leave_one_out_centroid(rows, DE1_RR_COLUMNS),
            "columns": DE1_RR_COLUMNS,
            "read": "DE-1 local dynamics over RR intervals only",
        },
        "de1_composite": {
            **leave_one_out_centroid(rows, DE1_COMPOSITE_COLUMNS),
            "columns": DE1_COMPOSITE_COLUMNS,
            "read": "DE-1 local dynamics over BPM plus RR",
        },
        "de1_with_mean": {
            **leave_one_out_centroid(rows, DE1_WITH_MEAN_COLUMNS),
            "columns": DE1_WITH_MEAN_COLUMNS,
            "read": "DE-1 dynamics plus mean-signal deltas",
        },
    }
    de1_accuracy = validations["de1_composite"]["accuracy"]
    hr_accuracy = validations["hr_only"]["accuracy"]
    if de1_accuracy > hr_accuracy:
        interpretation = (
            "DE-1 dynamics beats the mean-HR baseline on this pass, so the "
            "differential/local-dynamics lens has first-pass support on the "
            "existing Phase 12B HRV time series."
        )
    elif de1_accuracy == hr_accuracy:
        interpretation = (
            "DE-1 dynamics ties the mean-HR baseline on this pass. That keeps "
            "the lane plausible but not stronger than the simple comparator yet."
        )
    else:
        interpretation = (
            "DE-1 dynamics does not beat the mean-HR baseline on this pass; "
            "that is a useful limited/negative result and prevents overclaiming."
        )

    return {
        "status": "completed",
        "schema": "state / control / transform / invariant / drift / coherence / score",
        "validation_fork": "Nest 1 DE-1 -> Phase 12B HRV dynamics",
        "inputs": {"phase12b_path": str(phase12b_path), "hrv_root": str(hrv_root)},
        "session_count": len(rows),
        "condition_counts": dict(Counter(str(row["condition"]) for row in rows)),
        "blocked_or_skipped": blocked,
        "feature_sets": {
            "hr_only": HR_ONLY_COLUMNS,
            "de1_bpm_dynamics": DE1_BPM_COLUMNS,
            "de1_rr_dynamics": DE1_RR_COLUMNS,
            "de1_composite": DE1_COMPOSITE_COLUMNS,
            "de1_with_mean": DE1_WITH_MEAN_COLUMNS,
        },
        "validations": validations,
        "condition_summary": condition_summary(rows, ["delta_bpm_a", "delta_bpm_mean", "delta_rr_ms_a", "delta_rr_ms_mean"]),
        "interpretation": interpretation,
        "boundary": (
            "This is a real HRV time-series dynamics validation fork. It is not "
            "clinical biology, not EEG, and not a universal biological claim."
        ),
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Nest 1 DE-1 -> Phase 12B HRV Dynamics Validation Fork",
        "",
        f"Status: `{report['status']}`",
        "",
    ]
    if report["status"] == "blocked":
        lines.extend(
            [
                "This fork did not generate synthetic data.",
                "",
                "## Blocked Reasons",
                "",
            ]
        )
        lines.extend(f"- {reason}" for reason in report.get("blocked_reasons", []))
        lines.extend(["", f"Boundary: {report['boundary']}", ""])
        return "\n".join(lines)

    lines.extend(
        [
            "This is a real-data validation fork, not a validation note.",
            "It fits a bounded first-order local dynamics model to actual Phase 12B",
            "BPM and RR windows, then compares condition recovery against a simple",
            "mean-HR delta baseline.",
            "",
            "## Inputs",
            "",
            f"- Phase 12B canonical sessions: `{report['inputs']['phase12b_path']}`",
            f"- HRV session root: `{report['inputs']['hrv_root']}`",
            f"- sessions used: `{report['session_count']}`",
            f"- condition counts: `{report['condition_counts']}`",
            "",
            "## Leave-One-Out Class Recovery",
            "",
            "| Feature Set | Accuracy | Correct / Total | Read |",
            "| --- | ---: | ---: | --- |",
        ]
    )
    for key, label in (
        ("hr_only", "HR-only baseline"),
        ("de1_bpm_dynamics", "DE-1 BPM dynamics"),
        ("de1_rr_dynamics", "DE-1 RR dynamics"),
        ("de1_composite", "DE-1 composite dynamics"),
        ("de1_with_mean", "DE-1 dynamics + means"),
    ):
        result = report["validations"][key]
        lines.append(
            f"| {label} | {result['accuracy']} | {result['correct']} / {result['total']} | {result['read']} |"
        )

    lines.extend(
        [
            "",
            "## Condition Dynamics Snapshot",
            "",
            "| Condition | Runs | Mean delta BPM a | Mean delta BPM | Mean delta RR a | Mean delta RR |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for condition, summary in sorted(report["condition_summary"].items()):
        lines.append(
            "| "
            f"{condition} | {summary['runs']} | {summary['mean_delta_bpm_a']} | "
            f"{summary['mean_delta_bpm_mean']} | {summary['mean_delta_rr_ms_a']} | "
            f"{summary['mean_delta_rr_ms_mean']} |"
        )

    if report.get("blocked_or_skipped"):
        lines.extend(["", "## Skipped Rows", ""])
        lines.extend(f"- {item}" for item in report["blocked_or_skipped"])

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            report["interpretation"],
            "",
            "## Boundary",
            "",
            report["boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def run(phase12b_path: Path, hrv_root: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    if not phase12b_path.exists():
        return blocked_report(phase12b_path, hrv_root, out_dir, [f"missing {phase12b_path}"])
    if not hrv_root.exists():
        return blocked_report(phase12b_path, hrv_root, out_dir, [f"missing {hrv_root}"])

    rows, blocked = build_feature_rows(phase12b_path, hrv_root)
    if not rows:
        return blocked_report(phase12b_path, hrv_root, out_dir, blocked or ["no valid rows"])

    report = build_report(rows, blocked, phase12b_path, hrv_root)
    write_csv(out_dir / "de1_hrv_dynamics_features.csv", rows)
    (out_dir / "de1_hrv_dynamics_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (out_dir / "de1_hrv_dynamics_report.md").write_text(render_markdown(report), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase12b", type=Path, default=DEFAULT_PHASE12B)
    parser.add_argument("--hrv-root", type=Path, default=DEFAULT_HRV_ROOT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()
    report = run(args.phase12b, args.hrv_root, args.out_dir)
    print(json.dumps({"status": report["status"], "out_dir": str(args.out_dir)}, indent=2))


if __name__ == "__main__":
    main()
