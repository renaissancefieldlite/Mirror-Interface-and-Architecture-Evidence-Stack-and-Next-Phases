#!/usr/bin/env python3
"""Compare two V8 attention / MLP validation passes for repeatability."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE = (
    ROOT
    / "artifacts"
    / "validation"
    / "v8_attention_mlp_validation_all_models"
    / "v8_attention_mlp_validation_report.json"
)
DEFAULT_RERUN = (
    ROOT
    / "artifacts"
    / "validation"
    / "v8_attention_mlp_validation_all_models_rerun_02"
    / "v8_attention_mlp_validation_report.json"
)
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_attention_mlp_repeatability_all_models"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare V8 attention / MLP validation repeatability.")
    parser.add_argument("--base-report", default=str(DEFAULT_BASE), help="First validation report JSON.")
    parser.add_argument("--rerun-report", default=str(DEFAULT_RERUN), help="Rerun validation report JSON.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT), help="Output directory.")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing report: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def nested(report: dict[str, Any], *keys: str) -> Any:
    value: Any = report
    for key in keys:
        value = value[key]
    return value


def metric_pair(base: dict[str, Any], rerun: dict[str, Any], *keys: str) -> dict[str, Any]:
    first = nested(base, *keys)
    second = nested(rerun, *keys)
    result = {"base": first, "rerun": second}
    if isinstance(first, (int, float)) and isinstance(second, (int, float)):
        result["delta"] = round(float(second) - float(first), 9)
    return result


def build_report(base: dict[str, Any], rerun: dict[str, Any]) -> dict[str, Any]:
    same_status = base.get("status") == rerun.get("status")
    same_models = base.get("models") == rerun.get("models")
    same_rows = base.get("attention_rows") == rerun.get("attention_rows") and base.get("mlp_rows") == rerun.get("mlp_rows")
    attention_supported = (
        nested(base, "attention_flow", "status") == "attention_flow_supported_cross_model"
        and nested(rerun, "attention_flow", "status") == "attention_flow_supported_cross_model"
        and nested(base, "attention_flow", "weighted_attention_flow", "p_value_one_sided") <= 0.01
        and nested(rerun, "attention_flow", "weighted_attention_flow", "p_value_one_sided") <= 0.01
        and nested(base, "attention_flow", "weighted_minus_degree_score") > 0.0
        and nested(rerun, "attention_flow", "weighted_minus_degree_score") > 0.0
    )
    mlp_supported = (
        nested(base, "mlp_delta", "status") == "mlp_supported_cross_model"
        and nested(rerun, "mlp_delta", "status") == "mlp_supported_cross_model"
        and nested(base, "mlp_delta", "p_value_one_sided") <= 0.01
        and nested(rerun, "mlp_delta", "p_value_one_sided") <= 0.01
    )
    status = (
        "repeatability_supported"
        if same_status and same_models and same_rows and attention_supported and mlp_supported
        else "repeatability_partial_or_needs_review"
    )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "base_report": base.get("generated_at"),
        "rerun_report": rerun.get("generated_at"),
        "models": base.get("models"),
        "same_status": same_status,
        "same_models": same_models,
        "same_row_counts": same_rows,
        "attention_rows": metric_pair(base, rerun, "attention_rows"),
        "mlp_rows": metric_pair(base, rerun, "mlp_rows"),
        "attention_status": metric_pair(base, rerun, "attention_flow", "status"),
        "attention_weighted_score": metric_pair(base, rerun, "attention_flow", "weighted_attention_flow", "true_score"),
        "attention_weighted_p": metric_pair(
            base,
            rerun,
            "attention_flow",
            "weighted_attention_flow",
            "p_value_one_sided",
        ),
        "attention_degree_score": metric_pair(base, rerun, "attention_flow", "degree_only_baseline", "true_score"),
        "attention_weighted_minus_degree": metric_pair(base, rerun, "attention_flow", "weighted_minus_degree_score"),
        "mlp_status": metric_pair(base, rerun, "mlp_delta", "status"),
        "mlp_score": metric_pair(base, rerun, "mlp_delta", "true_score"),
        "mlp_p": metric_pair(base, rerun, "mlp_delta", "p_value_one_sided"),
        "clean_read": (
            "The all-exported-model attention / MLP gate repeated under the same prompt/model/export setup. "
            "Row counts, model set, support status, and shuffled-label control support are preserved; "
            "the rerun attention-flow and MLP scores remain positive and control-supported. "
            "This is repeatability of the validation result, not a claim of byte-identical internal floats."
        ),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 Attention / MLP All-Model Repeatability Report",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Scope",
        "",
        f"- models: `{', '.join(report['models'])}`",
        f"- same status: `{report['same_status']}`",
        f"- same model set: `{report['same_models']}`",
        f"- same row counts: `{report['same_row_counts']}`",
        "",
        "## Metrics",
        "",
        "| Metric | Base | Rerun | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    metric_names = [
        ("attention rows", "attention_rows"),
        ("MLP rows", "mlp_rows"),
        ("attention weighted score", "attention_weighted_score"),
        ("attention weighted p", "attention_weighted_p"),
        ("attention degree score", "attention_degree_score"),
        ("attention weighted-minus-degree", "attention_weighted_minus_degree"),
        ("MLP score", "mlp_score"),
        ("MLP p", "mlp_p"),
    ]
    for label, key in metric_names:
        item = report[key]
        lines.append(f"| {label} | `{item['base']}` | `{item['rerun']}` | `{item.get('delta', '')}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This closes the first repeatability gate for the same all-exported-model prompt set.",
            "- It does not yet close prompt-generalization; the next gate is a second independent prompt set.",
            "- `Nemotron` remains an interface-adapter row for this exporter path.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    base = load_json(Path(args.base_report).resolve())
    rerun = load_json(Path(args.rerun_report).resolve())
    report = build_report(base, rerun)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "v8_attention_mlp_repeatability_report.json"
    md_path = output_dir / "v8_attention_mlp_repeatability_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": report["status"], "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
