#!/usr/bin/env python3
"""GAME-1 real-trial gate.

This gate prepares and audits the trial data needed by
game1_adversarial_protocol_validation.py. It does not generate trial results.
Run with no inputs to write the trial template and a blocked report.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "game1_real_trial_gate"

TRIAL_FIELDS = [
    "trial_id",
    "run_id",
    "scenario_id",
    "condition",
    "agent_id",
    "objective",
    "perturbation_id",
    "task_success",
    "policy_consistency",
    "exploit_score",
    "drift_score",
    "stability_score",
    "transcript_uri",
    "scorer_id",
    "score_lock_date",
    "notes",
]
MANIFEST_TEMPLATE = {
    "status": "template_only",
    "task_family": "prompt_injection | routing_conflict | multi_agent_negotiation | fraud_like_decision | other",
    "mirror_condition_definition": "What changes under the mirror condition.",
    "control_condition_definition": "What stays baseline under the control condition.",
    "perturbation_schedule": "How adversarial or multi-agent pressure is assigned.",
    "scoring_lock": "Scoring rubric must be locked before scoring transcripts.",
    "minimum_rows": "At least 10 mirror rows and 10 control rows; larger is better.",
    "real_transcript_required": True,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv_header(path: Path, fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()


def write_templates(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv_header(out_dir / "game1_trials_template.csv", TRIAL_FIELDS)
    (out_dir / "game1_manifest_template.json").write_text(
        json.dumps(MANIFEST_TEMPLATE, indent=2), encoding="utf-8"
    )


def write_report(out_dir: Path, report: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "game1_real_trial_gate_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GAME-1 Real Trial Gate",
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
    if report.get("issues"):
        lines.extend(["", "## Issues", ""])
        for issue in report["issues"]:
            lines.append(f"- {issue}")
    lines.extend(["", "## Boundary", "", report["boundary"], ""])
    (out_dir / "game1_real_trial_gate_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def validate_trials(trial_csv: Path) -> tuple[dict, list[str]]:
    rows = read_csv(trial_csv)
    issues: list[str] = []
    conditions = {"mirror": 0, "control": 0}
    scenarios = set()
    perturbations = set()
    transcripts = 0
    scored_rows = 0
    numeric_fields = [
        "task_success",
        "policy_consistency",
        "exploit_score",
        "drift_score",
        "stability_score",
    ]
    required_text = [
        "trial_id",
        "scenario_id",
        "condition",
        "agent_id",
        "objective",
        "perturbation_id",
        "transcript_uri",
        "scorer_id",
        "score_lock_date",
    ]
    for index, row in enumerate(rows, start=2):
        for field in required_text:
            if not (row.get(field) or "").strip():
                issues.append(f"row {index} missing {field}")
        condition = (row.get("condition") or "").strip().lower()
        if condition in conditions:
            conditions[condition] += 1
        else:
            issues.append(f"row {index} condition must be mirror or control")
        if row.get("scenario_id"):
            scenarios.add(row["scenario_id"].strip())
        if row.get("perturbation_id"):
            perturbations.add(row["perturbation_id"].strip())
        if row.get("transcript_uri"):
            transcripts += 1
        numeric_ok = True
        for field in numeric_fields:
            number = to_float(row.get(field))
            if number is None:
                numeric_ok = False
                issues.append(f"row {index} missing numeric {field}")
            elif number < 0.0 or number > 1.0:
                numeric_ok = False
                issues.append(f"row {index} {field} must be in [0, 1]")
        if numeric_ok:
            scored_rows += 1

    if conditions["mirror"] < 10:
        issues.append("need at least 10 mirror-condition rows")
    if conditions["control"] < 10:
        issues.append("need at least 10 control-condition rows")
    if not perturbations:
        issues.append("need at least one adversarial or multi-agent perturbation_id")
    if transcripts < len(rows):
        issues.append("every trial row needs transcript_uri or evidence pointer")

    metrics = {
        "trial_rows": len(rows),
        "mirror_rows": conditions["mirror"],
        "control_rows": conditions["control"],
        "scenario_count": len(scenarios),
        "perturbation_count": len(perturbations),
        "rows_with_transcript_uri": transcripts,
        "fully_scored_rows": scored_rows,
    }
    return metrics, issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trial-csv", type=Path, help="Real GAME-1 trial CSV to audit.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--write-templates", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requirements = [
        "real mirror/control trial rows, not synthetic examples",
        "at least 10 mirror and 10 control rows",
        "declared adversarial or multi-agent perturbation schedule",
        "transcript_uri or evidence pointer for every row",
        "locked 0..1 scores for task_success, policy_consistency, exploit_score, drift_score, and stability_score",
    ]
    if args.write_templates or not args.trial_csv:
        write_templates(args.out_dir)
    if not args.trial_csv or not args.trial_csv.exists():
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_trial_csv",
                "read": "GAME-1 real-trial gate did not run because no real trial CSV was provided. Templates were written for the next collection pass.",
                "requirements": requirements,
                "boundary": "No GAME-1 validation was performed.",
            },
        )
        print(f"Wrote blocked report and templates to {args.out_dir}")
        return

    metrics, issues = validate_trials(args.trial_csv)
    status = "eligible_for_game1_validation" if not issues else "blocked_trial_pack_not_eligible"
    read = (
        "GAME-1 trial pack passed the real-trial gate and can be sent to game1_adversarial_protocol_validation.py."
        if not issues
        else "GAME-1 trial pack was audited but is not eligible for validation yet."
    )
    write_report(
        args.out_dir,
        {
            "status": status,
            "read": read,
            "requirements": requirements,
            "metrics": metrics,
            "issues": issues,
            "boundary": "This gate audits trial eligibility only; it does not score GAME-1 validation.",
        },
    )
    print(f"Wrote report to {args.out_dir}")


if __name__ == "__main__":
    main()
