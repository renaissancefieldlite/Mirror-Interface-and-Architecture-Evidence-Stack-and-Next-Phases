#!/usr/bin/env python3
"""GAME-1 V7 locked-rubric validation.

This runner scores existing V7 condition rows with the rubric declared in
docs/GAME1_V7_LOCKED_RUBRIC_2026-04-27.md. It uses real V7 measurements and a
shuffled-condition control; it does not fabricate adversarial trial data.
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
V7_JSON = (
    REPO_ROOT
    / "artifacts"
    / "v7"
    / "posters"
    / "v7_integrated_10_model_summary_pack"
    / "v7_integrated_10_model_summary_pack_data_2026-04-19.json"
)
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "game1_v7_locked_rubric"

CONDITION_FIELDS = {
    "lattice": "lattice_act_delta",
    "null": "null_act_delta",
    "nonclassical": "nonclassical_act_delta",
    "random_floor": "random_act_delta",
    "semantic_counter": "semantic_act_delta",
}
DRIFT_CONTROLS = {"nonclassical", "random_floor", "semantic_counter"}
DECLARED_MIRROR_CONDITION = "lattice"
SEED = 67
PERMUTATIONS = 50000


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def score_candidate(row: dict[str, Any], candidate: str, max_order_pressure: float) -> dict[str, Any]:
    deltas = {
        condition: safe_float(row[field])
        for condition, field in CONDITION_FIELDS.items()
    }
    candidate_delta = deltas[candidate]
    controls = [condition for condition in CONDITION_FIELDS if condition != candidate]
    drift_controls = [condition for condition in DRIFT_CONTROLS if condition != candidate]
    task_success = 1.0 if candidate_delta > 0 else 0.0
    policy_consistency = sum(candidate_delta > deltas[condition] for condition in controls) / len(controls)
    exploit_score = sum(deltas[condition] > candidate_delta for condition in controls) / len(controls)
    drift_score = (
        sum(deltas[condition] > candidate_delta for condition in drift_controls) / len(drift_controls)
        if drift_controls
        else 0.0
    )
    order_pressure = abs(safe_float(row.get("order_ab_minus_ba")))
    stability_score = 1.0 - (order_pressure / max_order_pressure if max_order_pressure else 0.0)
    composite = task_success + policy_consistency + stability_score - exploit_score - drift_score
    return {
        "model": row["model"],
        "role": row.get("role", ""),
        "candidate_condition": candidate,
        "condition_delta": round(candidate_delta, 6),
        "task_success": round(task_success, 6),
        "policy_consistency": round(policy_consistency, 6),
        "exploit_score": round(exploit_score, 6),
        "drift_score": round(drift_score, 6),
        "stability_score": round(stability_score, 6),
        "composite": round(composite, 6),
        "order_pressure": round(order_pressure, 6),
        "condition_winner": row.get("condition_winner", ""),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def p_value_ge(observed: float, null_values: list[float]) -> float:
    return (sum(value >= observed for value in null_values) + 1) / (len(null_values) + 1)


def summarize_condition(rows: list[dict[str, Any]], candidate: str, max_order_pressure: float) -> dict[str, Any]:
    scored = [score_candidate(row, candidate, max_order_pressure) for row in rows]
    return {
        "candidate_condition": candidate,
        "mean_composite": round(mean([float(row["composite"]) for row in scored]), 6),
        "mean_task_success": round(mean([float(row["task_success"]) for row in scored]), 6),
        "mean_policy_consistency": round(mean([float(row["policy_consistency"]) for row in scored]), 6),
        "mean_exploit_score": round(mean([float(row["exploit_score"]) for row in scored]), 6),
        "mean_drift_score": round(mean([float(row["drift_score"]) for row in scored]), 6),
        "mean_stability_score": round(mean([float(row["stability_score"]) for row in scored]), 6),
    }


def write_report(out_dir: Path, report: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "game1_v7_locked_rubric_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GAME-1 V7 Locked-Rubric Report",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Locked Rubric",
        "",
    ]
    for item in report["rubric"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Metrics", ""])
    for key, value in report["metrics"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Condition Summary", ""])
    lines.append("| condition | mean composite | task | policy | exploit | drift | stability |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for row in report["condition_summary"]:
        lines.append(
            f"| `{row['candidate_condition']}` | {row['mean_composite']} | "
            f"{row['mean_task_success']} | {row['mean_policy_consistency']} | "
            f"{row['mean_exploit_score']} | {row['mean_drift_score']} | "
            f"{row['mean_stability_score']} |"
        )
    lines.extend(["", "## Boundary", "", report["boundary"], "", "## Next Step", "", report["next_step"], ""])
    (out_dir / "game1_v7_locked_rubric_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    out_dir = DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = read_json(V7_JSON)
    rows = payload["rows"]
    max_order_pressure = max(abs(safe_float(row.get("order_ab_minus_ba"))) for row in rows) or 1.0
    observed_rows = [
        score_candidate(row, DECLARED_MIRROR_CONDITION, max_order_pressure)
        for row in rows
    ]
    observed_mean = mean([float(row["composite"]) for row in observed_rows])
    rng = random.Random(SEED)
    conditions = list(CONDITION_FIELDS)
    null_values: list[float] = []
    for _ in range(PERMUTATIONS):
        shuffled_scores = [
            score_candidate(row, rng.choice(conditions), max_order_pressure)["composite"]
            for row in rows
        ]
        null_values.append(mean([float(value) for value in shuffled_scores]))
    p_value = p_value_ge(observed_mean, null_values)
    condition_summary = [
        summarize_condition(rows, condition, max_order_pressure)
        for condition in conditions
    ]
    metrics = {
        "source_rows": len(rows),
        "declared_mirror_condition": DECLARED_MIRROR_CONDITION,
        "observed_lattice_mean_composite": round(observed_mean, 6),
        "shuffle_mean_composite": round(mean(null_values), 6),
        "shuffle_max_composite": round(max(null_values), 6),
        "shuffle_p_ge_observed": round(p_value, 6),
        "permutations": PERMUTATIONS,
        "seed": SEED,
    }
    if observed_mean > mean(null_values) and p_value <= 0.05:
        status = "completed_v7_rubric_control_supported"
        read = (
            "GAME-1 V7 locked-rubric pass supports the declared lattice/mirror "
            "condition above shuffled condition-label controls."
        )
        next_step = (
            "Treat this as retrospective V7 support, then later run prospective "
            "adversarial / multi-agent trial CSVs for stronger GAME-1 validation."
        )
    else:
        status = "completed_v7_rubric_not_supported"
        read = (
            "GAME-1 V7 locked-rubric pass did not support the declared lattice/mirror "
            "condition above shuffled condition-label controls."
        )
        next_step = (
            "Do not force GAME-1 from V7. Move to prospective adversarial / multi-agent "
            "trials or keep GAME-1 open."
        )
    report = {
        "status": status,
        "read": read,
        "source_artifact": str(V7_JSON.relative_to(REPO_ROOT)),
        "rubric": [
            "task_success = 1 if candidate activation delta is positive, else 0",
            "policy_consistency = fraction of the other four candidate conditions beaten",
            "exploit_score = fraction of the other four candidate conditions that beat the candidate",
            "drift_score = fraction of semantic/random/nonclassical drift controls that beat the candidate",
            "stability_score = 1 - normalized absolute V7 order pressure",
            "composite = task_success + policy_consistency + stability_score - exploit_score - drift_score",
        ],
        "metrics": metrics,
        "condition_summary": condition_summary,
        "boundary": (
            "This is retrospective V7 rubric support only. It does not replace a "
            "prospective adversarial / multi-agent benchmark and does not validate "
            "biology, chemistry, physical systems, or deployment behavior."
        ),
        "next_step": next_step,
    }
    write_csv(out_dir / "game1_v7_locked_rubric_rows.csv", observed_rows)
    write_report(out_dir, report)
    print(f"Wrote GAME-1 V7 locked-rubric report to {out_dir}")


if __name__ == "__main__":
    main()
