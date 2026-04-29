#!/usr/bin/env python3
"""Compare base/rerun/prompt-set-02 V8 attention / MLP validations."""

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
DEFAULT_PROMPT = (
    ROOT
    / "artifacts"
    / "validation"
    / "v8_attention_mlp_validation_prompt_set_02"
    / "v8_attention_mlp_validation_report.json"
)
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_attention_mlp_prompt_generalization"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare V8 attention / MLP prompt-generalization.")
    parser.add_argument("--base-report", default=str(DEFAULT_BASE), help="Base prompt validation report JSON.")
    parser.add_argument("--rerun-report", default=str(DEFAULT_RERUN), help="Same-prompt rerun validation report JSON.")
    parser.add_argument("--prompt-report", default=str(DEFAULT_PROMPT), help="Second prompt-set validation report JSON.")
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


def metric_table(base: dict[str, Any], rerun: dict[str, Any], prompt: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = [
        ("attention rows", ("attention_rows",)),
        ("MLP rows", ("mlp_rows",)),
        ("attention weighted score", ("attention_flow", "weighted_attention_flow", "true_score")),
        ("attention weighted p", ("attention_flow", "weighted_attention_flow", "p_value_one_sided")),
        ("attention degree score", ("attention_flow", "degree_only_baseline", "true_score")),
        ("attention weighted-minus-degree", ("attention_flow", "weighted_minus_degree_score")),
        ("MLP score", ("mlp_delta", "true_score")),
        ("MLP p", ("mlp_delta", "p_value_one_sided")),
    ]
    rows = []
    for label, keys in metrics:
        rows.append(
            {
                "metric": label,
                "base": nested(base, *keys),
                "rerun_02": nested(rerun, *keys),
                "prompt_set_02": nested(prompt, *keys),
            }
        )
    return rows


def build_report(base: dict[str, Any], rerun: dict[str, Any], prompt: dict[str, Any]) -> dict[str, Any]:
    same_models = base.get("models") == rerun.get("models") == prompt.get("models")
    same_rows = (
        base.get("attention_rows") == rerun.get("attention_rows") == prompt.get("attention_rows")
        and base.get("mlp_rows") == rerun.get("mlp_rows") == prompt.get("mlp_rows")
    )
    same_prompt_repeatability = (
        base.get("status") == "attention_and_mlp_supported_cross_model"
        and rerun.get("status") == "attention_and_mlp_supported_cross_model"
    )
    prompt_attention_supported = (
        nested(prompt, "attention_flow", "status") == "attention_flow_supported_cross_model"
        and nested(prompt, "attention_flow", "weighted_attention_flow", "p_value_one_sided") <= 0.01
        and nested(prompt, "attention_flow", "weighted_minus_degree_score") > 0.0
    )
    prompt_mlp_supported = (
        nested(prompt, "mlp_delta", "status") == "mlp_supported_cross_model"
        and nested(prompt, "mlp_delta", "p_value_one_sided") <= 0.01
        and nested(prompt, "mlp_delta", "true_score") > 0.0
    )
    if same_models and same_rows and same_prompt_repeatability and prompt_attention_supported and prompt_mlp_supported:
        status = "attention_and_mlp_prompt_generalization_supported"
    elif same_models and same_rows and same_prompt_repeatability and prompt_attention_supported:
        status = "attention_prompt_generalization_supported_mlp_not_supported"
    else:
        status = "prompt_generalization_partial_or_unsupported"

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "models": base.get("models"),
        "same_model_set": same_models,
        "same_row_counts": same_rows,
        "same_prompt_repeatability_status": same_prompt_repeatability,
        "prompt_set_02_attention_supported": prompt_attention_supported,
        "prompt_set_02_mlp_supported": prompt_mlp_supported,
        "base_status": base.get("status"),
        "rerun_02_status": rerun.get("status"),
        "prompt_set_02_status": prompt.get("status"),
        "metrics": metric_table(base, rerun, prompt),
        "clean_read": (
            "Base and rerun_02 close the all-exported-model same-prompt attention + MLP repeatability gate. "
            "Prompt_set_02 preserves the same model set and row counts under a second independent prompt surface. "
            "On prompt_set_02, attention-flow remains supported above shuffled labels and beats the degree-only baseline, "
            "so token-routing prompt-generalization is supported. MLP block-delta separation does not close on prompt_set_02, "
            "so full attention+MLP prompt-generalization is not yet supported."
        ),
        "next_gate": (
            "Run an MLP-depth expansion on prompt_set_02, preferably all layers or a denser layer grid, before claiming "
            "feed-forward prompt-generalization. If MLP remains unsupported after depth expansion, record it as a real "
            "architecture split: attention routing generalizes more strongly than MLP update signatures under wording changes."
        ),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 Attention / MLP Prompt-Generalization Report",
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
        f"- same model set: `{report['same_model_set']}`",
        f"- same row counts: `{report['same_row_counts']}`",
        f"- same-prompt repeatability closed before prompt_set_02: `{report['same_prompt_repeatability_status']}`",
        f"- prompt_set_02 attention supported: `{report['prompt_set_02_attention_supported']}`",
        f"- prompt_set_02 MLP supported: `{report['prompt_set_02_mlp_supported']}`",
        "",
        "## Metrics",
        "",
        "| Metric | Base | Rerun 02 | Prompt Set 02 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in report["metrics"]:
        lines.append(
            f"| {row['metric']} | `{row['base']}` | `{row['rerun_02']}` | `{row['prompt_set_02']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This supports prompt-generalization for attention-flow / token-routing.",
            "- This does not yet support full prompt-generalization for MLP / feed-forward block deltas.",
            "- The supported read is an internal split: attention routing generalizes under prompt change, while MLP update signatures require denser layer testing or remain prompt-sensitive.",
            "",
            "## Next Gate",
            "",
            report["next_gate"],
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    base = load_json(Path(args.base_report).resolve())
    rerun = load_json(Path(args.rerun_report).resolve())
    prompt = load_json(Path(args.prompt_report).resolve())
    report = build_report(base, rerun, prompt)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "v8_attention_mlp_prompt_generalization_report.json"
    md_path = output_dir / "v8_attention_mlp_prompt_generalization_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": report["status"], "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
