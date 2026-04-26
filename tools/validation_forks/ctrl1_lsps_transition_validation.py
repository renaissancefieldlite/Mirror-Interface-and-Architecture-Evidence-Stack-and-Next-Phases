#!/usr/bin/env python3
"""CTRL-1 LSPS transition-stability validation fork.

This runner validates a control-theory bridge only when real transition traces
exist. It expects a CSV of observed mode/control windows and scores stability
against declared expectations and simple churn/overshoot baselines.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "ctrl1_lsps_transition"


def write_report(out_dir: Path, report: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ctrl1_lsps_transition_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# CTRL-1 LSPS Transition Validation Fork",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Requirements",
        "",
    ]
    for item in report["requirements"]:
        lines.append(f"- {item}")
    if report.get("metrics"):
        lines.extend(["", "## Metrics", ""])
        for key, value in report["metrics"].items():
            lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Boundary", "", report["boundary"], ""])
    (out_dir / "ctrl1_lsps_transition_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def read_trace(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def to_float(value: str | None, default: float = 0.0) -> float:
    try:
        number = float(value) if value is not None else default
    except ValueError:
        return default
    return number if math.isfinite(number) else default


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(xs) != len(ys):
        return 0.0
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denom_x = sum((x - mean_x) ** 2 for x in xs)
    denom_y = sum((y - mean_y) ** 2 for y in ys)
    denominator = math.sqrt(denom_x * denom_y)
    return numerator / denominator if denominator else 0.0


def greater_equal_p_value(real: float, null_values: list[float]) -> float:
    if not null_values:
        return 1.0
    return (sum(1 for value in null_values if value >= real) + 1) / (len(null_values) + 1)


def score_trace(rows: list[dict[str, str]], permutations: int, seed: int) -> dict:
    usable = []
    for row in rows:
        mode = row.get("mode") or row.get("state") or row.get("observed_mode")
        expected = row.get("expected_mode") or row.get("target_mode")
        if not mode:
            continue
        usable.append(
            {
                "mode": mode,
                "expected_mode": expected or mode,
                "has_expected_mode": bool(expected),
                "stability_score": to_float(row.get("stability_score") or row.get("score"), 0.0),
                "expected_stability_score": to_float(row.get("expected_stability_score"), math.nan),
                "error": abs(to_float(row.get("error") or row.get("drift"), 0.0)),
            }
        )
    if not usable:
        return {"usable_rows": 0}

    transitions = sum(1 for left, right in zip(usable, usable[1:]) if left["mode"] != right["mode"])
    mode_counts = Counter(row["mode"] for row in usable)
    expected_hits = sum(1 for row in usable if row["mode"] == row["expected_mode"])
    scores = [row["stability_score"] for row in usable]
    errors = [row["error"] for row in usable]
    metrics = {
        "usable_rows": len(usable),
        "mode_count": len(mode_counts),
        "transition_count": transitions,
        "mode_churn_rate": round(transitions / max(1, len(usable) - 1), 4),
        "expected_mode_rows": sum(1 for row in usable if row["has_expected_mode"]),
        "expected_mode_accuracy": round(expected_hits / len(usable), 4),
        "mean_stability_score": round(sum(scores) / len(scores), 4),
        "mean_abs_error_or_drift": round(sum(errors) / len(errors), 4),
    }
    rng = random.Random(seed)
    expected_modes = [row["expected_mode"] for row in usable]
    observed_modes = [row["mode"] for row in usable]
    if len(set(expected_modes)) > 1 and len(set(observed_modes)) > 1:
        real_accuracy = expected_hits / len(usable)
        null_accuracies = []
        for _ in range(permutations):
            shuffled = expected_modes[:]
            rng.shuffle(shuffled)
            null_accuracies.append(
                sum(observed == expected for observed, expected in zip(observed_modes, shuffled))
                / len(usable)
            )
        metrics["expected_mode_accuracy_shuffle_p"] = round(
            greater_equal_p_value(real_accuracy, null_accuracies), 6
        )
        metrics["expected_mode_accuracy_shuffle_mean"] = round(
            sum(null_accuracies) / len(null_accuracies), 4
        )

    target_scores = [row["expected_stability_score"] for row in usable]
    if all(math.isfinite(value) for value in target_scores) and len(set(target_scores)) > 1:
        real_corr = pearson(target_scores, scores)
        null_corrs = []
        for _ in range(permutations):
            shuffled = scores[:]
            rng.shuffle(shuffled)
            null_corrs.append(pearson(target_scores, shuffled))
        metrics["stability_target_correlation"] = round(real_corr, 6)
        metrics["stability_target_correlation_shuffle_p"] = round(
            greater_equal_p_value(real_corr, null_corrs), 6
        )
        metrics["stability_target_correlation_shuffle_mean"] = round(
            sum(null_corrs) / len(null_corrs), 6
        )
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--trace-csv",
        type=Path,
        help="CSV with mode/state rows plus optional expected_mode, stability_score, error/drift columns.",
    )
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--permutations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=67)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requirements = [
        "real LSPS/orchestration transition trace CSV",
        "mode or state column for observed state",
        "expected_mode column for target/control comparison when available",
        "expected_stability_score column for numeric target/control comparison when available",
        "stability_score and/or error/drift column for bounded control scoring",
    ]
    if not args.trace_csv or not args.trace_csv.exists():
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_trace_csv",
                "read": "No real LSPS transition trace was provided, so CTRL-1 did not run.",
                "requirements": requirements,
                "boundary": "No LSPS/control validation was performed.",
            },
        )
        print(f"Wrote blocked report to {args.out_dir}")
        return

    metrics = score_trace(read_trace(args.trace_csv), args.permutations, args.seed)
    if metrics.get("usable_rows", 0) < 10:
        status = "blocked_insufficient_trace_rows"
        read = "Transition trace parsed, but fewer than 10 usable rows were available."
    elif (
        metrics.get("expected_mode_accuracy_shuffle_p", 1.0) <= 0.05
        or metrics.get("stability_target_correlation_shuffle_p", 1.0) <= 0.05
    ):
        status = "completed_control_supported"
        read = "CTRL-1 transition-stability validation completed with support above shuffled controls."
    else:
        status = "completed_no_control_support"
        read = "CTRL-1 transition-stability validation completed, but the declared controls were not beaten."

    write_report(
        args.out_dir,
        {
            "status": status,
            "read": read,
            "requirements": requirements,
            "metrics": metrics,
            "boundary": "This validates control-transition stability only; it does not validate biology, chemistry, or physical Bell claims.",
        },
    )
    print(f"Wrote report to {args.out_dir}")


if __name__ == "__main__":
    main()
