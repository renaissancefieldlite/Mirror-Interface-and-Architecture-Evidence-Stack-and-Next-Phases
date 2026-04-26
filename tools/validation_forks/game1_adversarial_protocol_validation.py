#!/usr/bin/env python3
"""GAME-1 adversarial / multi-agent stability validation fork.

This runner scores GAME-1 only when a real trial CSV exists. It expects paired
or repeated mirror/control trials under adversarial or multi-agent pressure and
compares stability, policy consistency, drift, and exploit resistance against
declared controls.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "game1_adversarial_protocol"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def to_float(value: str | None, default: float = 0.0) -> float:
    try:
        number = float(value) if value is not None else default
    except ValueError:
        return default
    return number if math.isfinite(number) else default


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def greater_equal_p_value(real: float, null_values: list[float]) -> float:
    if not null_values:
        return 1.0
    return (sum(1 for value in null_values if value >= real) + 1) / (len(null_values) + 1)


def normalize_condition(value: str) -> str:
    text = value.strip().lower()
    if text in {"mirror", "mirror_architecture", "lsps", "lattice"}:
        return "mirror"
    if text in {"control", "baseline", "naive", "standard"}:
        return "control"
    return text


def score_rows(rows: list[dict[str, str]], permutations: int, seed: int) -> dict:
    usable = []
    for row in rows:
        condition = normalize_condition(row.get("condition") or row.get("policy") or "")
        if condition not in {"mirror", "control"}:
            continue
        stability = to_float(row.get("stability_score") or row.get("stability"))
        consistency = to_float(row.get("policy_consistency") or row.get("consistency"))
        exploit = to_float(row.get("exploit_score") or row.get("exploit"))
        drift = to_float(row.get("drift_score") or row.get("drift"))
        task_success = to_float(row.get("task_success") or row.get("success"))
        composite = stability + consistency + task_success - exploit - drift
        usable.append(
            {
                "condition": condition,
                "stability": stability,
                "consistency": consistency,
                "exploit": exploit,
                "drift": drift,
                "task_success": task_success,
                "composite": composite,
            }
        )
    mirror = [row for row in usable if row["condition"] == "mirror"]
    control = [row for row in usable if row["condition"] == "control"]
    metrics = {
        "usable_rows": len(usable),
        "mirror_rows": len(mirror),
        "control_rows": len(control),
    }
    if len(mirror) < 10 or len(control) < 10:
        return metrics

    mirror_composite = [row["composite"] for row in mirror]
    control_composite = [row["composite"] for row in control]
    real_delta = mean(mirror_composite) - mean(control_composite)
    metrics.update(
        {
            "mirror_mean_composite": round(mean(mirror_composite), 6),
            "control_mean_composite": round(mean(control_composite), 6),
            "mirror_minus_control_composite": round(real_delta, 6),
            "mirror_mean_exploit": round(mean([row["exploit"] for row in mirror]), 6),
            "control_mean_exploit": round(mean([row["exploit"] for row in control]), 6),
            "mirror_mean_drift": round(mean([row["drift"] for row in mirror]), 6),
            "control_mean_drift": round(mean([row["drift"] for row in control]), 6),
        }
    )
    rng = random.Random(seed)
    composites = [row["composite"] for row in usable]
    labels = [row["condition"] for row in usable]
    mirror_count = len(mirror)
    null_deltas = []
    for _ in range(permutations):
        shuffled = labels[:]
        rng.shuffle(shuffled)
        shuffled_mirror = [score for score, label in zip(composites, shuffled) if label == "mirror"]
        shuffled_control = [score for score, label in zip(composites, shuffled) if label == "control"]
        if len(shuffled_mirror) == mirror_count and shuffled_control:
            null_deltas.append(mean(shuffled_mirror) - mean(shuffled_control))
    metrics["composite_delta_label_shuffle_p"] = round(
        greater_equal_p_value(real_delta, null_deltas), 6
    )
    metrics["composite_delta_label_shuffle_mean"] = round(mean(null_deltas), 6)
    return metrics


def write_report(out_dir: Path, report: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "game1_adversarial_protocol_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GAME-1 Adversarial / Multi-Agent Protocol Validation",
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
    (out_dir / "game1_adversarial_protocol_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trial-csv", type=Path, help="Real GAME-1 trial CSV.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--permutations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=67)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requirements = [
        "real trial CSV with mirror/control condition labels",
        "adversarial or multi-agent perturbation field",
        "task_success, policy_consistency, exploit_score, drift_score, and stability_score columns",
        "repeated trials with at least 10 mirror and 10 control rows",
    ]
    if not args.trial_csv or not args.trial_csv.exists():
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_trial_csv",
                "read": "No real adversarial / multi-agent trial CSV was provided, so GAME-1 did not run.",
                "requirements": requirements,
                "boundary": "No GAME-1 validation was performed.",
            },
        )
        print(f"Wrote blocked report to {args.out_dir}")
        return

    metrics = score_rows(read_csv(args.trial_csv), args.permutations, args.seed)
    if metrics.get("mirror_rows", 0) < 10 or metrics.get("control_rows", 0) < 10:
        status = "blocked_insufficient_trial_rows"
        read = "GAME-1 trial CSV parsed, but there are not enough mirror/control rows."
    elif metrics.get("composite_delta_label_shuffle_p", 1.0) <= 0.05:
        status = "completed_control_supported"
        read = "GAME-1 validation completed with mirror condition outperforming control above shuffled-label baseline."
    else:
        status = "completed_no_control_support"
        read = "GAME-1 validation completed, but mirror condition did not beat shuffled-label controls."
    write_report(
        args.out_dir,
        {
            "status": status,
            "read": read,
            "requirements": requirements,
            "metrics": metrics,
            "boundary": "This validates adversarial / multi-agent decision stability only; it does not validate biology, chemistry, or physical claims.",
        },
    )
    print(f"Wrote report to {args.out_dir}")


if __name__ == "__main__":
    main()
