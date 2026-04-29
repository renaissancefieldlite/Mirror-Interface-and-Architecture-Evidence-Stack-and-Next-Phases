#!/usr/bin/env python3
"""SPEC-1 -> Phase 12B HRV validation fork.

This is the first concrete Nest 1 validation fork. It moves beyond score schema
mapping by testing whether a formal spectral-method lens can recover measured
Phase 12B HRV condition classes from existing strap sessions.

No EEG is required for this pass. EEG becomes the richer follow-on layer.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.signal import welch


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
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "nest1_spec_phase12b_hrv"

FEATURE_COLUMNS = [
    "delta_mean_hr",
    "delta_rmssd",
    "delta_sdnn",
    "delta_lf_norm",
    "delta_hf_norm",
    "delta_lf_hf",
    "delta_log_total_power",
    "delta_dominant_frequency",
]

SPECTRAL_COLUMNS = [
    "delta_lf_norm",
    "delta_hf_norm",
    "delta_lf_hf",
    "delta_log_total_power",
    "delta_dominant_frequency",
]

TIME_COLUMNS = ["delta_mean_hr", "delta_rmssd", "delta_sdnn"]
HR_ONLY_COLUMNS = ["delta_mean_hr"]


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


def rmssd(rr_ms: np.ndarray) -> float:
    if len(rr_ms) < 3:
        return float("nan")
    diffs = np.diff(rr_ms)
    return float(np.sqrt(np.mean(diffs * diffs)))


def sdnn(rr_ms: np.ndarray) -> float:
    if len(rr_ms) < 2:
        return float("nan")
    return float(np.std(rr_ms, ddof=1))


def band_power(freqs: np.ndarray, power: np.ndarray, low: float, high: float) -> float:
    mask = (freqs >= low) & (freqs < high)
    if not np.any(mask):
        return 0.0
    return float(np.trapezoid(power[mask], freqs[mask]))


def window_features(samples: list[dict[str, float]], start: float, end: float) -> dict[str, float] | None:
    rows = [row for row in samples if start <= row["relative_seconds"] < end]
    if len(rows) < 16:
        return None

    times = np.array([row["relative_seconds"] - start for row in rows], dtype=float)
    rr = np.array([row["rr_ms"] for row in rows], dtype=float)
    bpm = np.array([row["bpm"] for row in rows], dtype=float)

    duration = max(float(times[-1] - times[0]), 1.0)
    fs = 4.0
    grid = np.arange(0.0, duration, 1.0 / fs)
    if len(grid) < 16:
        return None

    rr_interp = np.interp(grid, times, rr)
    rr_centered = rr_interp - np.mean(rr_interp)
    nperseg = min(256, max(16, len(rr_centered)))
    freqs, power = welch(rr_centered, fs=fs, nperseg=nperseg)

    lf = band_power(freqs, power, 0.04, 0.15)
    hf = band_power(freqs, power, 0.15, 0.40)
    total = lf + hf
    mask = (freqs >= 0.04) & (freqs <= 0.40)
    dominant_frequency = 0.0
    if np.any(mask):
        dominant_frequency = float(freqs[mask][np.argmax(power[mask])])

    return {
        "mean_hr": float(np.mean(bpm)),
        "rmssd": rmssd(rr),
        "sdnn": sdnn(rr),
        "lf_power": lf,
        "hf_power": hf,
        "total_power": total,
        "log_total_power": float(math.log1p(total)),
        "lf_norm": float(lf / total) if total > 0 else 0.0,
        "hf_norm": float(hf / total) if total > 0 else 0.0,
        "lf_hf": float(lf / hf) if hf > 0 else 0.0,
        "dominant_frequency": dominant_frequency,
        "rr_count": int(len(rr)),
    }


def session_windows(session_meta: dict) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    baseline_duration = float(session_meta["windows"]["baseline"]["duration_seconds"])
    condition_duration = float(session_meta["windows"]["condition"]["duration_seconds"])
    post_duration = float(session_meta["windows"]["post"]["duration_seconds"])
    baseline = (0.0, baseline_duration)
    condition = (baseline[1], baseline[1] + condition_duration)
    post = (condition[1], condition[1] + post_duration)
    return baseline, condition, post


def safe_delta(condition: dict[str, float], baseline: dict[str, float], key: str) -> float:
    left = condition.get(key, float("nan"))
    right = baseline.get(key, float("nan"))
    if math.isnan(left) or math.isnan(right):
        return float("nan")
    return left - right


def build_feature_rows(phase12b_path: Path, hrv_root: Path) -> list[dict[str, object]]:
    phase12b = load_json(phase12b_path)
    rows: list[dict[str, object]] = []
    for session in phase12b["canonical_sessions"]:
        session_id = session["session_id"]
        session_dir = hrv_root / session_id
        sample_path = session_dir / f"{session_id}_samples.csv"
        meta_path = session_dir / f"{session_id}.json"
        if not sample_path.exists() or not meta_path.exists():
            continue

        samples = load_samples(sample_path)
        meta = load_json(meta_path)
        baseline_range, condition_range, post_range = session_windows(meta)

        baseline_features = window_features(samples, *baseline_range)
        condition_features = window_features(samples, *condition_range)
        post_features = window_features(samples, *post_range)
        if not baseline_features or not condition_features or not post_features:
            continue

        row: dict[str, object] = {
            "condition": session["condition"],
            "run_label": session["run_label"],
            "run_index": session["run_index"],
            "session_id": session_id,
            "baseline_rr_count": baseline_features["rr_count"],
            "condition_rr_count": condition_features["rr_count"],
            "post_rr_count": post_features["rr_count"],
        }
        for key in ("mean_hr", "rmssd", "sdnn", "lf_norm", "hf_norm", "lf_hf", "log_total_power", "dominant_frequency"):
            row[f"baseline_{key}"] = baseline_features[key]
            row[f"condition_{key}"] = condition_features[key]
            row[f"delta_{key}"] = safe_delta(condition_features, baseline_features, key)
            row[f"post_delta_{key}"] = safe_delta(post_features, condition_features, key)
        rows.append(row)
    return rows


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
        return {"accuracy": 0.0, "predictions": [], "confusion": {}}

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
        confusion.setdefault(str(item["actual"]), {})
        confusion[str(item["actual"])][str(item["predicted"])] = (
            confusion[str(item["actual"])].get(str(item["predicted"]), 0) + 1
        )

    return {
        "accuracy": round(correct / len(rows), 3),
        "correct": correct,
        "total": len(rows),
        "predictions": predictions,
        "confusion": confusion,
    }


def mirror_margin(rows: list[dict[str, object]], columns: list[str], target: str = "mirror_coherence") -> dict:
    labels = [str(row["condition"]) for row in rows]
    x = matrix(rows, columns)
    margins = []
    for index, label in enumerate(labels):
        if label != target:
            continue
        train_indices = [i for i in range(len(rows)) if i != index]
        target_indices = [i for i in train_indices if labels[i] == target]
        control_indices = [i for i in train_indices if labels[i] != target]
        if not target_indices or not control_indices:
            continue
        target_centroid = np.mean(x[target_indices], axis=0)
        control_centroids = {
            control_label: np.mean(x[[i for i in control_indices if labels[i] == control_label]], axis=0)
            for control_label in sorted(set(labels) - {target})
            if [i for i in control_indices if labels[i] == control_label]
        }
        own_distance = float(np.linalg.norm(x[index] - target_centroid))
        nearest_control_label, nearest_control_distance = min(
            (
                (control_label, float(np.linalg.norm(x[index] - centroid)))
                for control_label, centroid in control_centroids.items()
            ),
            key=lambda item: item[1],
        )
        margins.append(
            {
                "run_label": rows[index]["run_label"],
                "own_distance": own_distance,
                "nearest_control": nearest_control_label,
                "nearest_control_distance": nearest_control_distance,
                "positive_margin": nearest_control_distance - own_distance,
            }
        )
    mean_margin = float(np.mean([item["positive_margin"] for item in margins])) if margins else 0.0
    positive_count = sum(1 for item in margins if item["positive_margin"] > 0)
    return {
        "target": target,
        "mean_positive_margin": round(mean_margin, 3),
        "positive_margin_count": positive_count,
        "total": len(margins),
        "rows": margins,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(report: dict) -> str:
    validations = report["validations"]
    lines = [
        "# Nest 1 SPEC-1 -> Phase 12B HRV Validation Fork",
        "",
        f"Status: `{report['status']}`",
        "",
        "This is a real-data validation fork, not just a validation note.",
        "It tests whether spectral-method features computed from existing HRV RR",
        "windows recover the Phase 12B condition labels better than simpler baselines.",
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
    for key, label in (
        ("hr_only", "HR-only baseline"),
        ("time_domain", "Time-domain HRV"),
        ("spectral_only", "SPEC-1 spectral"),
        ("mirror_composite", "Mirror composite"),
    ):
        result = validations[key]
        lines.append(
            f"| {label} | {result['accuracy']} | {result['correct']} / {result['total']} | {result['read']} |"
        )

    margin = report["mirror_margin"]
    lines.extend(
        [
            "",
            "## Mirror-Coherence Margin",
            "",
            f"- target: `{margin['target']}`",
            f"- positive margins: `{margin['positive_margin_count']} / {margin['total']}`",
            f"- mean positive margin: `{margin['mean_positive_margin']}`",
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


def build_report(rows: list[dict[str, object]], phase12b_path: Path, hrv_root: Path) -> dict:
    condition_counts = dict(Counter(str(row["condition"]) for row in rows))
    validations = {
        "hr_only": {
            **leave_one_out_centroid(rows, HR_ONLY_COLUMNS),
            "columns": HR_ONLY_COLUMNS,
            "read": "naive mean-HR delta comparator",
        },
        "time_domain": {
            **leave_one_out_centroid(rows, TIME_COLUMNS),
            "columns": TIME_COLUMNS,
            "read": "standard HRV time-domain delta comparator",
        },
        "spectral_only": {
            **leave_one_out_centroid(rows, SPECTRAL_COLUMNS),
            "columns": SPECTRAL_COLUMNS,
            "read": "formal SPEC-1 frequency / eigenmode-style comparator",
        },
        "mirror_composite": {
            **leave_one_out_centroid(rows, FEATURE_COLUMNS),
            "columns": FEATURE_COLUMNS,
            "read": "combined SPEC-1 plus HRV timing comparator",
        },
    }
    spectral_accuracy = validations["spectral_only"]["accuracy"]
    hr_accuracy = validations["hr_only"]["accuracy"]
    interpretation = (
        "SPEC-1 has support on this pass because spectral features recover condition "
        "labels at least as well as the HR-only baseline."
        if spectral_accuracy >= hr_accuracy
        else "SPEC-1 does not beat the HR-only baseline on this pass; that is a useful negative/limited result."
    )
    return {
        "status": "completed",
        "schema": "state / control / transform / invariant / drift / coherence / score",
        "validation_fork": "Nest 1 SPEC-1 -> Phase 12B HRV",
        "inputs": {
            "phase12b_path": str(phase12b_path),
            "hrv_root": str(hrv_root),
        },
        "session_count": len(rows),
        "condition_counts": condition_counts,
        "feature_columns": FEATURE_COLUMNS,
        "validations": validations,
        "mirror_margin": mirror_margin(rows, FEATURE_COLUMNS),
        "interpretation": interpretation,
        "boundary": (
            "This validates a formal spectral-method fork against existing HRV data only. "
            "It is not EEG validation, clinical validation, or chemistry validation."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase12b-json", type=Path, default=DEFAULT_PHASE12B)
    parser.add_argument("--hrv-root", type=Path, default=DEFAULT_HRV_ROOT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_feature_rows(args.phase12b_json, args.hrv_root)
    if not rows:
        raise SystemExit("No usable HRV rows found for SPEC-1 validation.")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(rows, args.phase12b_json, args.hrv_root)
    feature_csv = args.out_dir / "nest1_spec_phase12b_hrv_features.csv"
    report_json = args.out_dir / "nest1_spec_phase12b_hrv_report.json"
    report_md = args.out_dir / "nest1_spec_phase12b_hrv_report.md"

    write_csv(feature_csv, rows)
    report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report_md.write_text(render_markdown(report), encoding="utf-8")

    print(f"Wrote {feature_csv}")
    print(f"Wrote {report_json}")
    print(f"Wrote {report_md}")


if __name__ == "__main__":
    main()
