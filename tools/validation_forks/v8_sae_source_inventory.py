#!/usr/bin/env python3
"""Inventory SAE sources and V8 activation inputs.

This runner answers the first operational SAE question:

1. Do local pretrained / existing SAE assets already exist?
2. If not, do we have real V8 activation inputs suitable for bounded SAE
   training?

It does not train an SAE and does not validate SAE features. It records the
source decision that determines the next execution path.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_sae_source_inventory"
SAE_NAME_HINTS = ("sae", "sparse", "autoencoder", "transcoder")
SAE_EXTENSIONS = {".json", ".jsonl", ".csv", ".npz", ".pt", ".pth", ".safetensors"}


def is_sae_candidate(path: Path) -> bool:
    lower = path.name.lower()
    if path.suffix.lower() not in SAE_EXTENSIONS:
        return False
    return any(hint in lower for hint in SAE_NAME_HINTS)


def repo_sae_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if "v8_sae_feature_circuit_gate" in str(path):
            continue
        if "v8_sae_source_inventory" in str(path):
            continue
        if is_sae_candidate(path):
            candidates.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "bytes": path.stat().st_size,
                    "suffix": path.suffix.lower(),
                }
            )
    return candidates


def npz_shape(path: Path) -> dict[str, Any]:
    try:
        data = np.load(path, allow_pickle=True)
    except Exception as exc:  # pragma: no cover - report only
        return {"error": str(exc)}
    result: dict[str, Any] = {"path": str(path.relative_to(ROOT)), "arrays": {}}
    for key in data.files:
        value = data[key]
        result["arrays"][key] = {
            "shape": list(value.shape),
            "dtype": str(value.dtype),
        }
    if "points" in data.files:
        points = data["points"]
        result["row_count"] = int(points.shape[0])
        result["hidden_size"] = int(points.shape[1]) if len(points.shape) > 1 else None
    return result


def point_cloud_inputs() -> dict[str, Any]:
    compact_dir = ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "point_clouds"
    expanded_dir = ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "point_clouds_expanded"
    dense_dir = ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "point_clouds_dense_trajectory"
    dense = [npz_shape(path) for path in sorted(dense_dir.glob("*.npz"))]
    compact = [npz_shape(path) for path in sorted(compact_dir.glob("*.npz"))]
    expanded = [npz_shape(path) for path in sorted(expanded_dir.glob("*.npz"))]
    return {
        "compact_point_cloud_dir": str(compact_dir.relative_to(ROOT)),
        "compact_models": len(compact),
        "compact_total_rows": sum(int(item.get("row_count", 0)) for item in compact),
        "expanded_point_cloud_dir": str(expanded_dir.relative_to(ROOT)),
        "expanded_models": len(expanded),
        "expanded_total_rows": sum(int(item.get("row_count", 0)) for item in expanded),
        "dense_trajectory_dir": str(dense_dir.relative_to(ROOT)),
        "dense_models": len(dense),
        "dense_total_rows": sum(int(item.get("row_count", 0)) for item in dense),
        "dense_inputs": dense,
    }


def attention_mlp_inputs() -> dict[str, Any]:
    roots = sorted((ROOT / "artifacts" / "validation").glob("v8_attention_mlp_exports*"))
    rows = []
    for export_dir in roots:
        attention = export_dir / "v8_attention_topk_edges.csv"
        mlp = export_dir / "v8_mlp_block_deltas.csv"
        rows.append(
            {
                "path": str(export_dir.relative_to(ROOT)),
                "attention_rows": max(0, sum(1 for _ in attention.open("rb")) - 1) if attention.exists() else 0,
                "mlp_rows": max(0, sum(1 for _ in mlp.open("rb")) - 1) if mlp.exists() else 0,
            }
        )
    return {
        "export_dirs": rows,
        "export_dir_count": len(rows),
    }


def build_report() -> dict[str, Any]:
    sae_candidates = repo_sae_candidates()
    point_clouds = point_cloud_inputs()
    attention_mlp = attention_mlp_inputs()
    pretrained_ready = len(sae_candidates) > 0
    dense_ready = point_clouds["dense_models"] >= 2 and point_clouds["dense_total_rows"] > 0
    status = "pretrained_sae_available" if pretrained_ready else "bounded_training_inputs_ready" if dense_ready else "blocked_missing_sae_and_inputs"
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "pretrained_or_existing_sae_candidates": sae_candidates,
        "pretrained_or_existing_sae_count": len(sae_candidates),
        "v8_point_cloud_inputs": point_clouds,
        "attention_mlp_inputs": attention_mlp,
        "clean_read": (
            "No pretrained or existing SAE assets were detected in the public evidence repo. "
            "Real bounded SAE training inputs are present: GLM and Hermes dense trajectory point-clouds "
            "plus compact / expanded point-clouds for the wider model matrix. The next evidence-producing "
            "move is bounded SAE training/export on those real V8 activations, not SAE validation yet."
            if not pretrained_ready and dense_ready
            else "Existing SAE-like assets were detected and should be inspected before training a new bounded SAE."
            if pretrained_ready
            else "No existing SAE assets or sufficient dense activation inputs were detected."
        ),
        "next_execution_order": [
            "train bounded SAE pilot on GLM and Hermes dense trajectory point-cloud activations",
            "export feature activations with context, layer, token-role, and prompt-set labels",
            "build feature dictionaries from top activating token roles / contexts / layers",
            "construct feature-to-feature circuit edges across adjacent layers",
            "validate feature and circuit separation against shuffled labels and frequency / degree baselines",
        ]
        if not pretrained_ready and dense_ready
        else [
            "inspect detected SAE candidate files",
            "confirm model/layer compatibility with V8 activation exports",
            "run feature activation export if compatible",
        ],
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    inputs = report["v8_point_cloud_inputs"]
    lines = [
        "# V8 SAE Source Inventory",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Existing SAE Assets",
        "",
        f"- detected SAE-like candidate files: `{report['pretrained_or_existing_sae_count']}`",
    ]
    if report["pretrained_or_existing_sae_candidates"]:
        for item in report["pretrained_or_existing_sae_candidates"]:
            lines.append(f"- `{item['path']}` ({item['bytes']} bytes)")
    else:
        lines.append("- none detected outside the SAE protocol/gate files")
    lines.extend(
        [
            "",
            "## V8 Activation Inputs",
            "",
            f"- compact point-cloud models: `{inputs['compact_models']}`",
            f"- compact point-cloud total rows: `{inputs['compact_total_rows']}`",
            f"- expanded point-cloud models: `{inputs['expanded_models']}`",
            f"- expanded point-cloud total rows: `{inputs['expanded_total_rows']}`",
            f"- dense trajectory models: `{inputs['dense_models']}`",
            f"- dense trajectory total rows: `{inputs['dense_total_rows']}`",
            "",
            "### Dense Trajectory Inputs",
            "",
            "| Input | Rows | Hidden Size |",
            "| --- | ---: | ---: |",
        ]
    )
    for item in inputs["dense_inputs"]:
        lines.append(f"| `{item['path']}` | `{item.get('row_count')}` | `{item.get('hidden_size')}` |")
    lines.extend(["", "## Attention / MLP Companion Inputs", ""])
    for item in report["attention_mlp_inputs"]["export_dirs"]:
        lines.append(
            f"- `{item['path']}`: attention rows `{item['attention_rows']}`, MLP rows `{item['mlp_rows']}`"
        )
    lines.extend(["", "## Next Execution Order", ""])
    for index, item in enumerate(report["next_execution_order"], start=1):
        lines.append(f"{index}. {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    DEFAULT_OUT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    json_path = DEFAULT_OUT / "v8_sae_source_inventory_report.json"
    md_path = DEFAULT_OUT / "v8_sae_source_inventory_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": report["status"], "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
