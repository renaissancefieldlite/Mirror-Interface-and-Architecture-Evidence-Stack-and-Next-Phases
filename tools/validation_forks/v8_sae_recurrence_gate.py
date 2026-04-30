#!/usr/bin/env python3
"""SAE recurrence input gate.

This gate checks whether the real dense hidden-vector inputs exist for SAE
recurrence across base, rerun_02, and prompt_set_02. It records the current
state without fabricating recurrence exports from unmatched artifacts.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "artifacts" / "validation" / "v8_sae_recurrence_gate"


def file_state(path: Path) -> dict[str, Any]:
    files = sorted(path.glob("*.npz")) if path.exists() else []
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": path.exists(),
        "npz_count": len(files),
        "files": [str(file.relative_to(ROOT)) for file in files],
    }


def build_report() -> dict[str, Any]:
    base_dense = ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "point_clouds_dense_trajectory"
    candidate_dirs = {
        "base_dense": base_dense,
        "rerun_02_dense": ROOT
        / "artifacts"
        / "v8"
        / "residual_stream_bridge"
        / "point_clouds_dense_trajectory_rerun_02",
        "prompt_set_02_dense": ROOT
        / "artifacts"
        / "v8"
        / "residual_stream_bridge"
        / "point_clouds_dense_trajectory_prompt_set_02",
    }
    state = {name: file_state(path) for name, path in candidate_dirs.items()}
    base_ready = state["base_dense"]["npz_count"] >= 2
    rerun_ready = state["rerun_02_dense"]["npz_count"] >= 2
    prompt_ready = state["prompt_set_02_dense"]["npz_count"] >= 2
    status = (
        "sae_recurrence_inputs_ready"
        if base_ready and rerun_ready and prompt_ready
        else "sae_recurrence_input_pending_prompt_rerun_dense_vectors"
    )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "input_state": state,
        "clean_read": (
            "SAE recurrence can run once base, rerun_02, and prompt_set_02 dense hidden-vector point clouds exist "
            "for the same model/context structure. Base GLM/Hermes dense vectors exist; matching rerun_02 and "
            "prompt_set_02 dense vectors are the required next inputs."
            if status != "sae_recurrence_inputs_ready"
            else "Base, rerun_02, and prompt_set_02 dense hidden-vector point clouds are present for SAE recurrence."
        ),
        "next_gates": [
            "export rerun_02 dense trajectory point clouds for GLM / Hermes",
            "export prompt_set_02 dense trajectory point clouds for GLM / Hermes",
            "apply the bounded SAE encoder to those matched dense vectors",
            "compare feature recurrence across base, rerun_02, and prompt_set_02",
        ]
        if status != "sae_recurrence_inputs_ready"
        else [
            "run SAE recurrence export with the existing bounded SAE encoder",
            "validate feature recurrence across base, rerun_02, and prompt_set_02",
        ],
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 SAE Recurrence Gate",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Input State",
        "",
        "| Input | Exists | NPZ Count |",
        "| --- | ---: | ---: |",
    ]
    for name, item in report["input_state"].items():
        lines.append(f"| `{name}` | `{item['exists']}` | `{item['npz_count']}` |")
    lines.extend(["", "## Next Gates", ""])
    for item in report["next_gates"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    json_path = OUT_DIR / "v8_sae_recurrence_gate_report.json"
    md_path = OUT_DIR / "v8_sae_recurrence_gate_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": report["status"], "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
