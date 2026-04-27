#!/usr/bin/env python3
"""GAME-1 V7 condition crosswalk.

V7 already contains real stress/control-like conditions: lattice, null,
random-floor, semantic-counter, nonclassical, and order/non-commutativity.
This script maps those existing rows into the GAME-1 gate vocabulary without
pretending the locked GAME-1 score columns already existed.

Output status is intentionally conservative: crosswalk-ready, scoring-rubric
required.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
V7_JSON = (
    REPO_ROOT
    / "artifacts"
    / "v7"
    / "posters"
    / "v7_integrated_10_model_summary_pack"
    / "v7_integrated_10_model_summary_pack_data_2026-04-19.json"
)
DEFAULT_OUT_DIR = (
    REPO_ROOT / "artifacts" / "validation" / "game1_v7_condition_crosswalk"
)

CONDITION_FIELDS = {
    "lattice": "lattice_act_delta",
    "null": "null_act_delta",
    "nonclassical": "nonclassical_act_delta",
    "random_floor": "random_act_delta",
    "semantic_counter": "semantic_act_delta",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def make_condition_rows(v7_rows: list[dict]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in v7_rows:
        model = row["model"]
        for condition, field in CONDITION_FIELDS.items():
            output.append(
                {
                    "source_artifact": str(V7_JSON.relative_to(REPO_ROOT)),
                    "model": model,
                    "role": row.get("role", ""),
                    "v7_condition": condition,
                    "candidate_game_condition": "mirror" if condition == "lattice" else "control_or_perturbation",
                    "condition_delta": row.get(field),
                    "condition_winner": row.get("condition_winner"),
                    "order_direction": row.get("order_direction"),
                    "lattice_minus_null": row.get("lattice_minus_null"),
                    "lattice_minus_semantic": row.get("lattice_minus_semantic"),
                    "lattice_minus_random": row.get("lattice_minus_random"),
                    "available_for_game1": "condition_delta, condition_winner, order_direction",
                    "missing_for_game1_validation": (
                        "task_success, policy_consistency, exploit_score, "
                        "drift_score, stability_score, transcript_uri"
                    ),
                }
            )
        output.append(
            {
                "source_artifact": str(V7_JSON.relative_to(REPO_ROOT)),
                "model": model,
                "role": row.get("role", ""),
                "v7_condition": "order_noncommutativity",
                "candidate_game_condition": "perturbation_axis",
                "condition_delta": row.get("order_ab_minus_ba"),
                "condition_winner": row.get("condition_winner"),
                "order_direction": row.get("order_direction"),
                "lattice_minus_null": row.get("lattice_minus_null"),
                "lattice_minus_semantic": row.get("lattice_minus_semantic"),
                "lattice_minus_random": row.get("lattice_minus_random"),
                "available_for_game1": "order_ab_minus_ba, order_direction",
                "missing_for_game1_validation": (
                    "task_success, policy_consistency, exploit_score, "
                    "drift_score, stability_score, transcript_uri"
                ),
            }
        )
    return output


def make_candidate_rubric_rows(v7_rows: list[dict]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in v7_rows:
        # These are rubric candidates, not locked validation scores.
        lattice = float(row["lattice_act_delta"])
        null = float(row["null_act_delta"])
        semantic = float(row["semantic_act_delta"])
        random_floor = float(row["random_act_delta"])
        order_abs = abs(float(row["order_ab_minus_ba"]))
        mirror_vs_controls = lattice - max(null, semantic, random_floor)
        rows.append(
            {
                "model": row["model"],
                "role": row.get("role", ""),
                "candidate_mirror_advantage": round(mirror_vs_controls, 6),
                "candidate_null_margin": round(float(row["lattice_minus_null"]), 6),
                "candidate_semantic_margin": round(float(row["lattice_minus_semantic"]), 6),
                "candidate_random_margin": round(float(row["lattice_minus_random"]), 6),
                "candidate_order_pressure": round(order_abs, 6),
                "condition_winner": row.get("condition_winner"),
                "rubric_status": "candidate_only_not_validation",
            }
        )
    return rows


def summarize(v7_rows: list[dict], condition_rows: list[dict[str, object]]) -> dict:
    lattice_wins = sum(1 for row in v7_rows if row.get("condition_winner") == "lattice")
    semantic_or_random_wins = sum(
        1 for row in v7_rows if row.get("condition_winner") in {"semantic", "random"}
    )
    ab_order = sum(1 for row in v7_rows if row.get("order_direction") == "AB > BA")
    ba_order = sum(1 for row in v7_rows if row.get("order_direction") == "BA > AB")
    mirror_positive = sum(1 for row in v7_rows if float(row["lattice_act_delta"]) > 0)
    lattice_beats_null = sum(1 for row in v7_rows if float(row["lattice_minus_null"]) > 0)
    lattice_beats_semantic = sum(1 for row in v7_rows if float(row["lattice_minus_semantic"]) > 0)
    lattice_beats_random = sum(1 for row in v7_rows if float(row["lattice_minus_random"]) > 0)
    return {
        "source_rows": len(v7_rows),
        "crosswalk_condition_rows": len(condition_rows),
        "mirror_candidate_rows": sum(
            1 for row in condition_rows if row["candidate_game_condition"] == "mirror"
        ),
        "control_or_perturbation_rows": sum(
            1 for row in condition_rows if row["candidate_game_condition"] != "mirror"
        ),
        "lattice_positive_rows": mirror_positive,
        "lattice_winner_rows": lattice_wins,
        "semantic_or_random_winner_rows": semantic_or_random_wins,
        "lattice_beats_null_rows": lattice_beats_null,
        "lattice_beats_semantic_rows": lattice_beats_semantic,
        "lattice_beats_random_rows": lattice_beats_random,
        "order_ab_gt_ba_rows": ab_order,
        "order_ba_gt_ab_rows": ba_order,
    }


def write_report(out_dir: Path, report: dict) -> None:
    (out_dir / "game1_v7_condition_crosswalk_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GAME-1 V7 Condition Crosswalk",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Metrics",
        "",
    ]
    for key, value in report["metrics"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## What This Adds",
            "",
            report["adds"],
            "",
            "## What Is Still Missing",
            "",
        ]
    )
    for item in report["missing"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            report["boundary"],
            "",
            "## Next Step",
            "",
            report["next_step"],
            "",
        ]
    )
    (out_dir / "game1_v7_condition_crosswalk_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    out_dir = DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = read_json(V7_JSON)
    v7_rows = payload["rows"]
    condition_rows = make_condition_rows(v7_rows)
    rubric_rows = make_candidate_rubric_rows(v7_rows)
    write_csv(out_dir / "game1_v7_condition_crosswalk_raw.csv", condition_rows)
    write_csv(out_dir / "game1_v7_candidate_rubric_not_validation.csv", rubric_rows)
    metrics = summarize(v7_rows, condition_rows)
    report = {
        "status": "crosswalk_ready_scoring_rubric_required",
        "read": (
            "V7 contains real adversarial/control-like condition structure that can seed GAME-1, "
            "but it was not originally scored with GAME-1 task_success / consistency / exploit / drift / stability columns."
        ),
        "source_artifact": str(V7_JSON.relative_to(REPO_ROOT)),
        "outputs": {
            "raw_crosswalk_csv": "artifacts/validation/game1_v7_condition_crosswalk/game1_v7_condition_crosswalk_raw.csv",
            "candidate_rubric_csv": "artifacts/validation/game1_v7_condition_crosswalk/game1_v7_candidate_rubric_not_validation.csv",
        },
        "metrics": metrics,
        "adds": (
            "GAME-1 is no longer a vague future lane. Existing V7 lattice/null/random/semantic/"
            "nonclassical/order conditions are mapped into a concrete adversarial-condition surface."
        ),
        "missing": [
            "locked rubric mapping from V7 deltas into GAME-1 score columns",
            "explicit task_success and policy_consistency scores",
            "explicit exploit_score and drift_score scores",
            "transcript/evidence pointers at trial-row granularity",
            "a preregistered threshold before claiming GAME-1 validation",
        ],
        "boundary": (
            "This is a real-data crosswalk, not a GAME-1 validation. It does not prove adversarial/"
            "multi-agent stability until the scoring rubric is locked and run against eligible trial rows."
        ),
        "next_step": (
            "Lock a retrospective V7 scoring rubric as exploratory-only, or run a new small real GAME-1 "
            "mirror/control adversarial task pack with the score columns declared before scoring."
        ),
    }
    write_report(out_dir, report)
    print(f"Wrote GAME-1 V7 condition crosswalk to {out_dir}")


if __name__ == "__main__":
    main()
