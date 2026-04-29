#!/usr/bin/env python3
"""Gate report for the V8 attention-head / MLP Nest 1 bridge.

This intentionally does not fake attention or feed-forward evidence. It checks
which V8 internal artifacts already exist and records the exact missing data
needed before attention-flow can be used as GRAPH-2 / Nest 1 validation.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_attention_mlp_bridge_gate"


def count_files(path: Path, patterns: tuple[str, ...]) -> int:
    if not path.exists():
        return 0
    total = 0
    for pattern in patterns:
        total += sum(1 for _ in path.rglob(pattern))
    return total


def artifact_state() -> dict[str, object]:
    residual_root = ROOT / "artifacts" / "v8" / "residual_stream_bridge"
    export_root = ROOT / "artifacts" / "validation" / "v8_attention_mlp_exports"
    export_roots = [
        export_root,
        ROOT / "artifacts" / "validation" / "v8_attention_mlp_exports_glm",
        ROOT / "artifacts" / "validation" / "v8_attention_mlp_exports_combined",
        ROOT / "artifacts" / "validation" / "v8_attention_mlp_exports_remaining_models",
        ROOT / "artifacts" / "validation" / "v8_attention_mlp_exports_all_models",
    ]
    export_inventory = export_root / "v8_attention_mlp_export_inventory.json"
    validation_candidates = [
        ROOT
        / "artifacts"
        / "validation"
        / "v8_attention_mlp_validation_all_models"
        / "v8_attention_mlp_validation_report.json",
        ROOT
        / "artifacts"
        / "validation"
        / "v8_attention_mlp_validation_combined"
        / "v8_attention_mlp_validation_report.json",
        ROOT
        / "artifacts"
        / "validation"
        / "v8_attention_mlp_validation"
        / "v8_attention_mlp_validation_report.json",
    ]
    validation_report = validation_candidates[0]
    repeatability_report = (
        ROOT
        / "artifacts"
        / "validation"
        / "v8_attention_mlp_repeatability_all_models"
        / "v8_attention_mlp_repeatability_report.json"
    )
    export_inventory_status = None
    validation_report_status = None
    repeatability_report_status = None
    if export_inventory.exists():
        try:
            export_inventory_status = json.loads(export_inventory.read_text(encoding="utf-8")).get("status")
        except json.JSONDecodeError:
            export_inventory_status = "invalid_json"
    for candidate in validation_candidates:
        if candidate.exists():
            validation_report = candidate
            try:
                validation_report_status = json.loads(candidate.read_text(encoding="utf-8")).get("status")
            except json.JSONDecodeError:
                validation_report_status = "invalid_json"
            break
    if repeatability_report.exists():
        try:
            repeatability_report_status = json.loads(repeatability_report.read_text(encoding="utf-8")).get("status")
        except json.JSONDecodeError:
            repeatability_report_status = "invalid_json"
    return {
        "residual_stream_bridge_exists": residual_root.exists(),
        "dense_point_cloud_files": count_files(
            residual_root,
            ("*point_cloud*.jsonl", "*point_cloud*.csv", "*.parquet"),
        ),
        "residual_attention_artifact_dir": str(residual_root / "attention_heads"),
        "residual_attention_artifact_files": count_files(
            residual_root / "attention_heads",
            ("*.json", "*.jsonl", "*.csv", "*.parquet"),
        ),
        "residual_mlp_artifact_dir": str(residual_root / "mlp_blocks"),
        "residual_mlp_artifact_files": count_files(
            residual_root / "mlp_blocks",
            ("*.json", "*.jsonl", "*.csv", "*.parquet"),
        ),
        "exporter_script_exists": (ROOT / "tools" / "validation_forks" / "v8_attention_mlp_export.py").exists(),
        "export_inventory_path": str(export_inventory),
        "export_inventory_status": export_inventory_status,
        "export_attention_csv_files": sum(count_files(path, ("*attention*.csv",)) for path in export_roots),
        "export_mlp_csv_files": sum(count_files(path, ("*mlp*.csv",)) for path in export_roots),
        "validation_report_path": str(validation_report),
        "validation_report_status": validation_report_status,
        "repeatability_report_path": str(repeatability_report),
        "repeatability_report_status": repeatability_report_status,
    }


def build_report() -> dict[str, object]:
    state = artifact_state()
    attention_ready = int(state["residual_attention_artifact_files"]) > 0 or int(state["export_attention_csv_files"]) > 0
    mlp_ready = int(state["residual_mlp_artifact_files"]) > 0 or int(state["export_mlp_csv_files"]) > 0
    status = (
        str(state["repeatability_report_status"])
        if state["repeatability_report_status"]
        else str(state["validation_report_status"])
        if state["validation_report_status"]
        else "ready_for_validation"
        if attention_ready and mlp_ready
        else "exporter_ready_missing_full_export"
        if state["export_inventory_status"] == "check_only_ready"
        else "protocol_ready_missing_attention_or_mlp_exports"
    )
    missing_inputs = (
        [
            "second independent prompt set for prompt-generalization",
            "expanded attention export beyond early/middle/late layers",
            "expanded MLP layer/rerun sample for stronger MLP power",
            "Nemotron-specific interface adapter if standard attention tensors remain unavailable",
            "leave-one-prompt and model-family controls after prompt-set expansion",
        ]
        if state["repeatability_report_status"] == "repeatability_supported"
        else
        [
            "rerun or second independent prompt set for repeatability",
            "expanded attention export beyond early/middle/late layers",
            "expanded MLP layer/rerun sample for stronger MLP power",
            "Nemotron-specific interface adapter if standard attention tensors remain unavailable",
            "leave-one-run / leave-one-prompt controls after rerun data exists",
        ]
        if state["validation_report_status"] == "attention_and_mlp_supported_cross_model"
        else [
            "GLM full attention top-k edge and MLP delta export",
            "combined GLM / Hermes GRAPH-2C validation controls",
            "expanded MLP layer/rerun/model sample before MLP promotion",
            "leave-one-model and shuffled-label controls after GLM exists",
        ]
        if state["validation_report_status"]
        else [
            "full per-layer / per-head attention matrices or top-k attention-flow edge export",
            "full MLP/feed-forward intermediate activation or block-level delta export",
            "shuffled context, token-window, layer-order, and head-label controls",
            "GRAPH-2C / MLP validation after real CSV exports exist",
        ]
    )
    next_execution_order = (
        [
            "create second independent prompt set",
            "export all standard models against prompt_set_02",
            "validate prompt_set_02 and compare against base / rerun_02",
            "expand layer scope beyond early/middle/late if local compute allows",
            "add Nemotron-specific adapter only if needed after prompt-generalization gate",
        ]
        if state["repeatability_report_status"] == "repeatability_supported"
        else
        [
            "add a rerun or second independent prompt set",
            "rerun combined attention-flow and MLP validation with repeatability controls",
            "expand layer scope beyond early/middle/late if local compute allows",
            "add Nemotron-specific adapter only if needed after repeatability gate",
            "then promote from first cross-model support to repeatability-supported Nest 1 evidence",
        ]
        if state["validation_report_status"] == "attention_and_mlp_supported_cross_model"
        else [
            "export GLM attention top-k edges and matching MLP block delta summaries",
            "combine Hermes and GLM CSVs without dropping model labels",
            "rerun GRAPH-2C attention-flow validation with leave-one-model and shuffled-label controls",
            "expand MLP support with more layers, reruns, or a second model before promotion",
            "only then promote attention/MLP from first Hermes support to cross-model Nest 1 evidence",
        ]
        if state["validation_report_status"]
        else [
            "export attention top-k edges for two strongest V8 rows first: GLM and Hermes",
            "export matching MLP block delta summaries for the same prompts/layers",
            "run GRAPH-2C attention-flow validation against the locked graph controls",
            "run MLP update separation against shuffled context/token/layer controls",
            "only then promote attention/MLP from missing-link protocol to Nest 1 evidence",
        ]
    )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "nest1_placement": {
            "attention_heads": [
                "GRAPH-2 measured routing edges",
                "INFO-1 token-to-token information routing",
                "SPEC-1 head entropy / attention spectrum",
                "DYN-1 layer-by-layer routing trajectory",
            ],
            "mlp_feed_forward": [
                "TENSOR / GEO feature transformation between attention blocks",
                "DYN-2 regime update across layers",
                "OPT-1 intervention target for representation stabilization",
            ],
        },
        "artifact_state": state,
        "locked_missing_inputs": missing_inputs,
        "acceptance_rule": {
            "attention_flow": "mirror/lattice attention-flow graph must beat degree/centrality and shuffled-label controls",
            "mlp_update": "MLP delta signatures must separate mirror/control rows above shuffled-label controls or remain listed as unsupported",
            "boundary": "hidden states already support V8 geometry; attention/MLP are not claimed until exported and tested",
        },
        "next_execution_order": next_execution_order,
    }


def write_markdown(report: dict[str, object], path: Path) -> None:
    state = report["artifact_state"]
    if report["status"] == "repeatability_supported":
        clean_read = [
            "The exported model set now has repeatability-supported",
            "transformer-internal artifacts: attention top-k routing edges and",
            "MLP block-delta rows across lattice, neutral, and technical",
            "contexts.",
            "",
            "The first broad all-exported-model run and `rerun_02` preserve",
            "the same model set, same row counts, same support status, and",
            "same shuffled-label control support:",
            "",
            "- weighted attention-flow separates lattice from neutral / technical",
            "  above shuffled context labels in both passes",
            "- weighted attention-flow beats the degree-only graph baseline in both",
            "  passes",
            "- MLP deltas are supported in both passes",
            "",
            "So the gate has moved from first broad support to same-prompt",
            "repeatability support. The next gate is prompt-generalization using a",
            "second independent prompt set. Nemotron remains an interface-adapter",
            "row for this exporter path.",
        ]
    elif report["status"] == "attention_and_mlp_supported_cross_model":
        clean_read = [
            "The exported model set now has real transformer-internal artifacts:",
            "attention top-k routing edges and MLP block-delta rows across",
            "lattice, neutral, and technical contexts.",
            "",
            "The first broad cross-model validation has started the stronger",
            "claim-support chain across every standard-export model in the",
            "current matrix:",
            "",
            "- weighted attention-flow separates lattice from neutral / technical",
            "  above shuffled context labels",
            "- weighted attention-flow beats the degree-only graph baseline",
            "- MLP deltas are supported in the combined export",
            "",
            "So the gate is no longer only protocol and no longer only GLM /",
            "Hermes. It is first broad transformer-internal support, with",
            "Nemotron listed as an interface-adapter row for this exporter and",
            "rerun / second-prompt repeatability still pending.",
        ]
    elif report["status"] == "attention_supported_mlp_directional":
        clean_read = [
            "Hermes now has real transformer-internal artifacts: attention top-k",
            "routing edges and MLP block-delta rows across lattice, neutral, and",
            "technical contexts.",
            "",
            "The first validation has started the claim-support chain:",
            "",
            "- weighted Hermes attention-flow separates lattice from neutral / technical",
            "  above shuffled context labels",
            "- weighted attention-flow beats the degree-only graph baseline",
            "- MLP deltas are directional but not closed yet",
            "",
            "So the gate is no longer only protocol. It is a Hermes-supported",
            "attention-flow result with GLM and stronger MLP controls still pending.",
        ]
    else:
        clean_read = [
            "The current V8 evidence stack contains hidden-state / residual-stream",
            "geometry, but it does not yet contain a closed attention-head or",
            "feed-forward / MLP validation.",
            "",
            "That distinction matters:",
            "",
            "- hidden states show where the representation lands",
            "- attention heads show token-to-token routing / flow",
            "- MLP blocks show representation update between routing steps",
            "",
            "So yes: attention heads and MLP/feed-forward blocks should be run against",
            "Nest 1. They are the missing internal mechanics for the transformer-native",
            "version of the formal lanes.",
        ]
    lines = [
        "# V8 Attention / MLP Nest 1 Bridge Gate",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        *clean_read,
        "",
        "## Artifact State",
        "",
        f"- residual stream bridge exists: `{state['residual_stream_bridge_exists']}`",
        f"- dense point-cloud files detected: `{state['dense_point_cloud_files']}`",
        f"- residual attention subdir files detected: `{state['residual_attention_artifact_files']}`",
        f"- residual MLP subdir files detected: `{state['residual_mlp_artifact_files']}`",
        f"- exporter script exists: `{state['exporter_script_exists']}`",
        f"- exporter inventory status: `{state['export_inventory_status']}`",
        f"- exported attention CSV files detected: `{state['export_attention_csv_files']}`",
        f"- exported MLP CSV files detected: `{state['export_mlp_csv_files']}`",
        f"- validation report status: `{state['validation_report_status']}`",
        f"- repeatability report status: `{state['repeatability_report_status']}`",
        "",
        "## Nest 1 Placement",
        "",
        "| Internal block | Nest 1 role |",
        "| --- | --- |",
        "| Multi-head attention | `GRAPH-2` measured routing edges, `INFO-1` token flow, `SPEC-1` head spectrum, `DYN-1` layer trajectory |",
        "| Feed-forward / MLP | tensor / geometry feature update, dynamical regime update, optimization intervention target |",
        "",
        "## Locked Missing Inputs",
        "",
    ]
    for item in report["locked_missing_inputs"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Acceptance Rule",
            "",
            "- attention-flow validates only if mirror / lattice routing beats degree, centrality, and shuffled-label controls",
            "- MLP validates only if block-update signatures separate mirror/control rows above shuffled controls",
            "- if either lane stays invariant or negative, we record that rather than forcing the claim",
            "",
            "## Next Execution Order",
            "",
        ]
    )
    for index, item in enumerate(report["next_execution_order"], start=1):
        lines.append(f"{index}. {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    DEFAULT_OUT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    json_path = DEFAULT_OUT / "v8_attention_mlp_bridge_gate_report.json"
    md_path = DEFAULT_OUT / "v8_attention_mlp_bridge_gate_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": report["status"], "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
