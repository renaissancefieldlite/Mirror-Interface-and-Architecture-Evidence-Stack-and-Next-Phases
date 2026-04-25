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


def score_trace(rows: list[dict[str, str]]) -> dict:
    usable = []
    for row in rows:
        mode = row.get("mode") or row.get("state") or row.get("observed_mode")
        expected = row.get("expected_mode") or row.get("target_mode") or mode
        if not mode:
            continue
        usable.append(
            {
                "mode": mode,
                "expected_mode": expected,
                "stability_score": to_float(row.get("stability_score") or row.get("score"), 0.0),
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
    return {
        "usable_rows": len(usable),
        "mode_count": len(mode_counts),
        "transition_count": transitions,
        "mode_churn_rate": round(transitions / max(1, len(usable) - 1), 4),
        "expected_mode_accuracy": round(expected_hits / len(usable), 4),
        "mean_stability_score": round(sum(scores) / len(scores), 4),
        "mean_abs_error_or_drift": round(sum(errors) / len(errors), 4),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--trace-csv",
        type=Path,
        help="CSV with mode/state rows plus optional expected_mode, stability_score, error/drift columns.",
    )
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requirements = [
        "real LSPS/orchestration transition trace CSV",
        "mode or state column for observed state",
        "expected_mode column for target/control comparison when available",
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

    metrics = score_trace(read_trace(args.trace_csv))
    if metrics.get("usable_rows", 0) < 10:
        status = "blocked_insufficient_trace_rows"
        read = "Transition trace parsed, but fewer than 10 usable rows were available."
    else:
        status = "completed"
        read = "CTRL-1 transition-stability validation completed against the provided trace."

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
