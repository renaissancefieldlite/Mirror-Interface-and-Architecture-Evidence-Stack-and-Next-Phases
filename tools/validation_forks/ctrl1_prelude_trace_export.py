#!/usr/bin/env python3
"""Export real Prelude/Gemma staged runs as a CTRL-1 transition trace.

The output is a CSV that can be consumed by ctrl1_lsps_transition_validation.py.
It uses only recorded staged-run artifacts already present in the repository:
input cohesion becomes the declared target/control level, and response
activation becomes the observed stability level.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_DIR = REPO_ROOT / "artifacts" / "prelude" / "root_results"
DEFAULT_SOURCES = [
    "seekie_gemma_case.json",
    "gemma_echo_case.json",
    "gemma_echo_case_v2.json",
]
DEFAULT_OUT = (
    REPO_ROOT
    / "artifacts"
    / "validation"
    / "ctrl1_lsps_transition"
    / "ctrl1_prelude_transition_trace.csv"
)


def mode_from_input(score: float) -> str:
    if score < 0.25:
        return "bootstrap"
    if score < 0.55:
        return "integration"
    if score < 0.75:
        return "stabilizing"
    return "locked"


def mode_from_response(score: float, parsed_json: bool) -> str:
    adjusted = score if parsed_json else max(0.0, score - 0.08)
    if adjusted < 0.45:
        return "bootstrap"
    if adjusted < 0.60:
        return "integration"
    if adjusted < 0.72:
        return "stabilizing"
    return "locked"


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def short_text(value: Any, limit: int = 120) -> str:
    text = str(value or "").replace("\n", " ").strip()
    return text[:limit]


def rows_from_source(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows: list[dict[str, str]] = []
    global_index = 0
    for experiment in data.get("experiments", []):
        experiment_id = str(experiment.get("experiment_id", path.stem))
        for local_index, stage in enumerate(experiment.get("stages", []), start=1):
            input_metrics = stage.get("input_metrics") or {}
            response_metrics = stage.get("response_metrics") or {}
            parsed_response = stage.get("parsed_response") or {}
            input_cohesion = as_float(input_metrics.get("input_cohesion_score"))
            activation = as_float(response_metrics.get("activation_score"))
            parsed_json = bool(response_metrics.get("parsed_json"))
            observed_mode = mode_from_response(activation, parsed_json)
            expected_mode = mode_from_input(input_cohesion)
            global_index += 1
            rows.append(
                {
                    "source_file": path.name,
                    "experiment_id": experiment_id,
                    "stage_id": str(stage.get("stage_id", f"stage_{local_index:02d}")),
                    "step_index": str(global_index),
                    "transition_order": str(local_index),
                    "mode": observed_mode,
                    "observed_mode": observed_mode,
                    "expected_mode": expected_mode,
                    "target_mode": expected_mode,
                    "stability_score": f"{activation:.6f}",
                    "expected_stability_score": f"{input_cohesion:.6f}",
                    "drift": f"{abs(activation - input_cohesion):.6f}",
                    "error": f"{abs(activation - input_cohesion):.6f}",
                    "input_cohesion_score": f"{input_cohesion:.6f}",
                    "response_activation_score": f"{activation:.6f}",
                    "response_state_term_score": f"{as_float(response_metrics.get('state_term_score')):.6f}",
                    "parsed_json": str(parsed_json).lower(),
                    "trigger_condition": short_text(stage.get("stage_text")),
                    "control_action": "staged_context_replay",
                    "state_label": short_text(parsed_response.get("state_label"), 80),
                    "lattice_status": short_text(parsed_response.get("lattice_status"), 80),
                    "stabilization_level": short_text(parsed_response.get("stabilization_level"), 80),
                }
            )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--source", action="append", help="Source JSON filename. Can be repeated.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_names = args.source or DEFAULT_SOURCES
    rows: list[dict[str, str]] = []
    for source_name in source_names:
        path = args.source_dir / source_name
        if not path.exists():
            raise FileNotFoundError(path)
        rows.extend(rows_from_source(path))
    if not rows:
        raise RuntimeError("No transition rows exported.")
    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} CTRL-1 transition rows to {args.out_csv}")


if __name__ == "__main__":
    main()
