#!/usr/bin/env python3
"""CAT-1 composition / transfer benchmark."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE6_JSON = REPO_ROOT / "artifacts" / "v8" / "phase6_pennylane_encoding" / "v8_phase6_pennylane_encoding_data_2026-04-22.json"
PHASE7_JSON = REPO_ROOT / "artifacts" / "v8" / "phase7_qiskit_mirror" / "v8_phase7_qiskit_mirror_data_2026-04-22.json"
OPT1_REPORT = REPO_ROOT / "artifacts" / "validation" / "opt1_perspective_nest_benchmark" / "opt1_perspective_nest_benchmark_report.json"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "cat1_composition_transfer_benchmark"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_float(value: Any, digits: int = 12) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(numeric):
        return 0.0
    return round(numeric, digits)


def pair_rank_rows(labels: list[str], matrix: np.ndarray) -> list[dict[str, Any]]:
    rows = []
    for left_index, left in enumerate(labels):
        for right_index, right in enumerate(labels):
            if left_index < right_index:
                rows.append(
                    {
                        "pair": "/".join(sorted((left, right))),
                        "score": float(matrix[left_index, right_index]),
                    }
                )
    return sorted(rows, key=lambda row: row["score"], reverse=True)


def matrix_transfer_block(
    labels: list[str],
    source_matrix: list[list[float]],
    target_matrix: list[list[float]],
) -> dict[str, Any]:
    source = np.array(source_matrix, dtype=float)
    target = np.array(target_matrix, dtype=float)
    delta = np.abs(source - target)
    source_rank = pair_rank_rows(labels, source)
    target_rank = pair_rank_rows(labels, target)
    source_top3 = {row["pair"] for row in source_rank[:3]}
    target_top3 = {row["pair"] for row in target_rank[:3]}
    return {
        "max_abs_delta": clean_float(np.max(delta)),
        "mean_abs_delta": clean_float(np.mean(delta)),
        "source_top_pair": source_rank[0]["pair"],
        "target_top_pair": target_rank[0]["pair"],
        "top_pair_preserved": int(source_rank[0]["pair"] == target_rank[0]["pair"]),
        "top3_overlap": len(source_top3 & target_top3),
        "top3_source": ", ".join(row["pair"] for row in source_rank[:3]),
        "top3_target": ", ".join(row["pair"] for row in target_rank[:3]),
    }


def write_report(out_dir: Path, report: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "cat1_composition_transfer_benchmark_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# CAT-1 Composition / Transfer Benchmark",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## PennyLane -> Qiskit Transfer",
        "",
    ]
    for name, block in report["implementation_transfer"].items():
        lines.append(f"### {name}")
        lines.append("")
        for key, value in block.items():
            lines.append(f"- `{key}`: `{value}`")
        lines.append("")
    lines.extend(["## Hardware Subset Transfer", ""])
    for key, value in report["hardware_subset_transfer"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Boundary", "", report["boundary"], "", "## Next Step", "", report["next_step"], ""])
    (out_dir / "cat1_composition_transfer_benchmark_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    out_dir = DEFAULT_OUT_DIR
    phase6 = read_json(PHASE6_JSON)
    phase7 = read_json(PHASE7_JSON)
    opt1 = read_json(OPT1_REPORT)
    labels = [str(row["model"]) for row in phase6["models"]]
    implementation_transfer = {
        "angle": matrix_transfer_block(
            labels,
            phase6["angle_fidelity_matrix"],
            phase7["qiskit_angle_fidelity_matrix"],
        ),
        "amplitude": matrix_transfer_block(
            labels,
            phase6["amplitude_fidelity_matrix"],
            phase7["qiskit_amplitude_fidelity_matrix"],
        ),
    }
    angle_ok = (
        implementation_transfer["angle"]["max_abs_delta"] <= 1e-12
        and implementation_transfer["angle"]["top_pair_preserved"] == 1
    )
    amplitude_ok = (
        implementation_transfer["amplitude"]["max_abs_delta"] <= 1e-12
        and implementation_transfer["amplitude"]["top_pair_preserved"] == 1
    )
    hardware = opt1["hardware_pair_optimization"]
    hardware_subset_transfer = {
        "source": str(OPT1_REPORT.relative_to(REPO_ROOT)),
        "phase6_best_pair": hardware["phase6_best_pair"],
        "hardware_best_pair": hardware["hardware_best_pair"],
        "best_pair_agreement": hardware["best_pair_agreement"],
        "status": hardware["status"],
    }
    if angle_ok and amplitude_ok and int(hardware["best_pair_agreement"]) == 1:
        status = "completed_implementation_composition_supported_hardware_partial"
        read = (
            "CAT-1 composition transfer is supported at the PennyLane -> Qiskit "
            "implementation layer, with hardware-subset best-pair agreement still "
            "marked small-N partial."
        )
    else:
        status = "completed_composition_transfer_not_closed"
        read = "CAT-1 did not preserve the declared relation chain strongly enough to close."
    report = {
        "status": status,
        "read": read,
        "implementation_transfer": implementation_transfer,
        "hardware_subset_transfer": hardware_subset_transfer,
        "boundary": (
            "This validates relation preservation across encoded software implementations "
            "and a small hardware subset. It does not prove universal cross-domain "
            "composition or full physical transfer."
        ),
        "next_step": (
            "Expand hardware-executed feature circuits and then move to Nest 2 real "
            "molecular / allostery validation for external-domain composition."
        ),
    }
    write_report(out_dir, report)
    print(f"Wrote CAT-1 composition transfer benchmark to {out_dir}")


if __name__ == "__main__":
    main()
