#!/usr/bin/env python3
"""Gate report for the V8 SAE feature/circuit proof layer.

This is a readiness and acceptance-rule gate. It does not synthesize SAE
features or fake circuit traces. It records the exact artifacts required before
Sparse Autoencoder (SAE) features can be promoted into the V8 evidence stack.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_sae_feature_circuit_gate"


def count_files(path: Path, patterns: tuple[str, ...]) -> int:
    if not path.exists():
        return 0
    total = 0
    for pattern in patterns:
        total += sum(1 for _ in path.rglob(pattern))
    return total


def artifact_state() -> dict[str, object]:
    export_root = ROOT / "artifacts" / "validation" / "v8_sae_feature_circuit_exports"
    validation_root = ROOT / "artifacts" / "validation" / "v8_sae_feature_circuit_validation"
    report_path = validation_root / "v8_sae_feature_circuit_validation_report.json"
    validation_status = None
    if report_path.exists():
        try:
            validation_status = json.loads(report_path.read_text(encoding="utf-8")).get("status")
        except json.JSONDecodeError:
            validation_status = "invalid_json"
    return {
        "export_dir": str(export_root),
        "validation_dir": str(validation_root),
        "sae_model_files": count_files(export_root / "sae_models", ("*.json", "*.pt", "*.safetensors", "*.npz")),
        "feature_activation_files": count_files(
            export_root,
            ("*feature_activation*.csv", "*feature_activation*.jsonl", "*sae_feature*.csv", "*sae_feature*.jsonl"),
        ),
        "feature_dictionary_files": count_files(
            export_root,
            ("*feature_dictionary*.json", "*feature_dictionary*.csv", "*feature_labels*.json", "*feature_labels*.csv"),
        ),
        "circuit_edge_files": count_files(
            export_root,
            ("*circuit_edge*.csv", "*circuit_edge*.jsonl", "*feature_circuit*.csv", "*feature_circuit*.jsonl"),
        ),
        "ablation_files": count_files(export_root, ("*ablation*.csv", "*ablation*.json", "*ablation*.jsonl")),
        "validation_report_path": str(report_path),
        "validation_report_status": validation_status,
    }


def build_report() -> dict[str, object]:
    state = artifact_state()
    feature_ready = int(state["feature_activation_files"]) > 0
    circuit_ready = int(state["circuit_edge_files"]) > 0
    dictionary_ready = int(state["feature_dictionary_files"]) > 0
    status = (
        str(state["validation_report_status"])
        if state["validation_report_status"]
        else "ready_for_validation"
        if feature_ready and circuit_ready and dictionary_ready
        else "protocol_ready_missing_sae_exports"
    )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "artifact_state": state,
        "proof_layer": {
            "residual_stream": "where the representation lands",
            "attention_flow": "which tokens route into which tokens / heads",
            "mlp_feed_forward": "how representation updates between routing steps",
            "sae_features": "which sparse interpretable features activate and form circuits",
        },
        "required_export_schema": {
            "feature_activations": [
                "model",
                "prompt_set",
                "context",
                "layer_index",
                "layer_depth",
                "token_index",
                "token_role",
                "feature_id",
                "activation",
                "sparsity",
            ],
            "feature_dictionary": [
                "model",
                "layer_index",
                "feature_id",
                "top_tokens_or_terms",
                "human_label_optional",
                "decoder_norm",
            ],
            "feature_circuit_edges": [
                "model",
                "prompt_set",
                "context",
                "source_layer",
                "source_feature_id",
                "target_layer",
                "target_feature_id",
                "edge_weight",
                "edge_type",
            ],
            "optional_ablation": [
                "model",
                "prompt_set",
                "context",
                "ablated_feature_or_edge",
                "readout_delta",
                "hidden_state_delta",
            ],
        },
        "acceptance_rule": {
            "feature_layer": (
                "lattice / mirror feature activations must separate from neutral / technical controls "
                "above shuffled context labels and feature-frequency baselines"
            ),
            "circuit_layer": (
                "feature-to-feature circuit paths must beat degree / centrality baselines and shuffled "
                "feature-label or shuffled-token-window controls"
            ),
            "prompt_generalization": (
                "supported SAE features or circuits must recur across base, rerun_02, and prompt_set_02 "
                "before claiming prompt-generalized feature/circuit structure"
            ),
            "ablation": (
                "optional stronger closeout: ablating top SAE features or circuit edges should move "
                "readout/hidden-state signatures more than matched control ablations"
            ),
        },
        "locked_missing_inputs": [
            "SAE feature activation export for the same standard model/prompt/context matrix",
            "feature dictionary or top-token labels for each exported SAE feature",
            "feature-to-feature circuit edge export across layers",
            "shuffled-label, shuffled-feature, shuffled-token-window, and degree/centrality controls",
            "optional ablation pass for causal circuit support",
        ],
        "next_execution_order": [
            "choose available SAE source: pretrained local SAEs if present, otherwise train bounded SAEs on exported V8 activations",
            "export feature activations for base, rerun_02, and prompt_set_02 on the standard model set",
            "build feature dictionaries and topic labels for Mirror Interface / LSPS, quantum consciousness geometry, circuit-state bridge, neutral controls, and technical controls",
            "construct feature-circuit edges across token roles and layers",
            "validate feature separation and circuit-flow against locked controls",
            "only then promote SAE from protocol gate to evidence layer",
        ],
    }


def write_markdown(report: dict[str, object], path: Path) -> None:
    state = report["artifact_state"]
    lines = [
        "# V8 SAE Feature / Circuit Gate",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        "Sparse Autoencoder features are the next interpretable proof layer after",
        "hidden states, attention-flow, and MLP/feed-forward deltas.",
        "",
        "The role is specific:",
        "",
        "- hidden states show where the representation lands",
        "- attention heads show token-routing flow",
        "- MLP blocks show representation updates",
        "- SAE features expose sparse interpretable feature activations and possible circuit paths",
        "",
        "This gate is protocol-ready, not evidence-closed. No SAE feature/circuit",
        "claim is promoted until real SAE activations, feature dictionaries, circuit",
        "edges, and controls exist.",
        "",
        "## Artifact State",
        "",
        f"- SAE model files: `{state['sae_model_files']}`",
        f"- feature activation files: `{state['feature_activation_files']}`",
        f"- feature dictionary files: `{state['feature_dictionary_files']}`",
        f"- circuit edge files: `{state['circuit_edge_files']}`",
        f"- ablation files: `{state['ablation_files']}`",
        f"- validation report status: `{state['validation_report_status']}`",
        "",
        "## Required Exports",
        "",
    ]
    for name, fields in report["required_export_schema"].items():
        lines.append(f"- `{name}`: {', '.join(f'`{field}`' for field in fields)}")
    lines.extend(["", "## Acceptance Rule", ""])
    for name, rule in report["acceptance_rule"].items():
        lines.append(f"- `{name}`: {rule}")
    lines.extend(["", "## Locked Missing Inputs", ""])
    for item in report["locked_missing_inputs"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Execution Order", ""])
    for index, item in enumerate(report["next_execution_order"], start=1):
        lines.append(f"{index}. {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    DEFAULT_OUT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    json_path = DEFAULT_OUT / "v8_sae_feature_circuit_gate_report.json"
    md_path = DEFAULT_OUT / "v8_sae_feature_circuit_gate_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": report["status"], "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
