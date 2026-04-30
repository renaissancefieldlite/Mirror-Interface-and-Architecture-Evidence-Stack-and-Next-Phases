#!/usr/bin/env python3
"""MLP-only depth export for prompt_set_02.

The earlier prompt_set_02 attention/MLP export used the early/middle/late layer
grid. This runner focuses only on MLP/feed-forward modules so every available
MLP layer can be exported without requesting full attention tensors again.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import torch


TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parents[1]
sys.path.insert(0, str(TOOLS_DIR))

from v8_attention_mlp_export import (  # noqa: E402
    DEFAULT_HF_HOME,
    DEFAULT_HF_MODULES_CACHE,
    MLP_FIELDS,
    checkpoint_overrides,
    discover_mlp_modules,
    first_tensor,
    layer_depth_label,
    load_model,
    resolve_checkpoint,
    resolve_device,
    select_models,
    selected_contexts,
    summarize_mlp_delta,
)


DEFAULT_MANIFEST = (
    ROOT
    / "artifacts"
    / "v8"
    / "residual_stream_bridge"
    / "v8_residual_stream_manifest_prompt_set_02_2026-04-29.json"
)
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_mlp_depth_prompt_set_02"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export MLP-only prompt_set_02 depth rows.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Prompt-set manifest JSON.")
    parser.add_argument("--results-dir", default=str(DEFAULT_OUT), help="Output directory.")
    parser.add_argument("--model", action="append", default=[], help="Display model name. Repeatable.")
    parser.add_argument("--context", action="append", default=[], help="Context label. Defaults to all manifest contexts.")
    parser.add_argument("--checkpoint", action="append", help="Override checkpoint as DisplayName=/path.")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "mps"], help="Torch device.")
    parser.add_argument("--dtype", default="auto", choices=["auto", "float32", "float16", "bfloat16"], help="Torch dtype.")
    parser.add_argument("--max-length", type=int, default=384, help="Maximum prompt tokens.")
    parser.add_argument("--check-only", action="store_true", help="Only write readiness inventory.")
    return parser.parse_args()


def readiness_inventory(
    manifest: dict[str, Any],
    selected_model_names: set[str],
    overrides: dict[str, str],
    selected_context_names: set[str],
) -> list[dict[str, Any]]:
    inventory = []
    for model_item in select_models(manifest, selected_model_names):
        checkpoint = resolve_checkpoint(model_item, overrides)
        contexts = selected_contexts(model_item, selected_context_names)
        inventory.append(
            {
                "display_name": model_item.get("display_name"),
                "checkpoint": checkpoint,
                "checkpoint_status": "ready" if checkpoint else "missing_checkpoint",
                "contexts": [context.get("context") for context in contexts],
                "context_count": len(contexts),
            }
        )
    return inventory


def export_mlp_rows(args: argparse.Namespace, manifest: dict[str, Any], selected_models: set[str], selected_contexts_set: set[str], overrides: dict[str, str]) -> dict[str, Any]:
    results_dir = Path(args.results_dir).resolve()
    results_dir.mkdir(parents=True, exist_ok=True)
    mlp_path = results_dir / "v8_mlp_depth_prompt_set_02.csv"
    device = resolve_device(args.device)
    rows_written = 0
    model_summaries = []

    with mlp_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MLP_FIELDS, lineterminator="\n")
        writer.writeheader()

        for model_item in select_models(manifest, selected_models):
            checkpoint = resolve_checkpoint(model_item, overrides)
            if checkpoint is None:
                model_summaries.append(
                    {
                        "model": model_item.get("display_name"),
                        "status": "missing_checkpoint",
                        "mlp_modules": 0,
                        "contexts": 0,
                        "rows": 0,
                    }
                )
                continue
            tokenizer, model = load_model(checkpoint, device=device, dtype_choice=args.dtype)
            contexts = selected_contexts(model_item, selected_contexts_set)
            mlp_modules = discover_mlp_modules(model)
            total_layers = max(mlp_modules.keys()) + 1 if mlp_modules else 0
            model_rows = 0

            for context in contexts:
                prompt = context["prompt"]
                encoded = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=args.max_length)
                input_ids = encoded["input_ids"].to(device)
                attention_mask = encoded.get("attention_mask")
                if attention_mask is not None:
                    attention_mask = attention_mask.to(device)
                token_count = int(input_ids.shape[-1])
                captured: dict[int, tuple[str, Any, Any]] = {}
                handles = []

                def make_hook(layer_index: int, module_name: str):
                    def hook(_module: Any, hook_input: Any, hook_output: Any) -> None:
                        if first_tensor(hook_input) is not None and first_tensor(hook_output) is not None:
                            captured[layer_index] = (module_name, hook_input, hook_output)

                    return hook

                for layer_index, (module_name, module) in sorted(mlp_modules.items()):
                    handles.append(module.register_forward_hook(make_hook(layer_index, module_name)))
                with torch.no_grad():
                    model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        output_attentions=False,
                        output_hidden_states=False,
                        use_cache=False,
                    )
                for handle_obj in handles:
                    handle_obj.remove()

                for layer_index, (module_name, hook_input, hook_output) in sorted(captured.items()):
                    row = summarize_mlp_delta(
                        model_name=model_item["display_name"],
                        context_name=context["context"],
                        layer_index=layer_index,
                        total_layers=total_layers,
                        module_name=module_name,
                        hook_input=hook_input,
                        hook_output=hook_output,
                        token_count=token_count,
                    )
                    if row:
                        writer.writerow(row)
                        rows_written += 1
                        model_rows += 1
            model_summaries.append(
                {
                    "model": model_item.get("display_name"),
                    "status": "exported",
                    "mlp_modules": len(mlp_modules),
                    "contexts": len(contexts),
                    "rows": model_rows,
                }
            )
            del model
            if device == "mps":
                torch.mps.empty_cache()

    return {"mlp_depth_csv": str(mlp_path), "mlp_rows": rows_written, "model_summaries": model_summaries}


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# V8 MLP Depth Prompt Set 02 Export",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Scope",
        "",
        f"- manifest: `{report['manifest']}`",
        f"- selected models: `{', '.join(report['selected_models']) or 'all'}`",
        f"- selected contexts: `{', '.join(report['selected_contexts']) or 'all'}`",
        f"- device: `{report['device']}`",
        f"- max length: `{report['max_length']}`",
        "",
        "## Inventory",
        "",
        "| Model | Checkpoint status | Contexts |",
        "| --- | --- | --- |",
    ]
    for item in report["inventory"]:
        lines.append(
            f"| {item['display_name']} | `{item['checkpoint_status']}` | {', '.join(item['contexts'])} |"
        )
    if report.get("exports"):
        lines.extend(["", "## Exported Rows", "", "| Model | MLP modules | Contexts | Rows |", "| --- | ---: | ---: | ---: |"])
        for item in report["exports"]["model_summaries"]:
            lines.append(f"| {item['model']} | `{item['mlp_modules']}` | `{item['contexts']}` | `{item['rows']}` |")
        lines.extend(
            [
                "",
                f"- MLP depth CSV: `{report['exports']['mlp_depth_csv']}`",
                f"- total rows: `{report['exports']['mlp_rows']}`",
            ]
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    DEFAULT_HF_MODULES_CACHE.mkdir(parents=True, exist_ok=True)
    DEFAULT_HF_HOME.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected_models = set(args.model or [])
    selected_contexts_set = set(args.context or [])
    overrides = checkpoint_overrides(args.checkpoint)
    output_dir = Path(args.results_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory = readiness_inventory(manifest, selected_models, overrides, selected_contexts_set)
    status = "check_only_ready"
    exports = None
    if not args.check_only:
        exports = export_mlp_rows(args, manifest, selected_models, selected_contexts_set, overrides)
        status = "export_complete" if exports["mlp_rows"] else "blocked_no_mlp_rows"
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "manifest": str(manifest_path),
        "selected_models": [item["display_name"] for item in inventory if item["checkpoint_status"] == "ready"],
        "selected_contexts": sorted(selected_contexts_set),
        "device": resolve_device(args.device),
        "dtype": args.dtype,
        "max_length": args.max_length,
        "inventory": inventory,
        "exports": exports,
        "clean_read": (
            "MLP-depth prompt_set_02 export is complete. This artifact expands the feed-forward gate from the earlier "
            "early/middle/late sample into every available MLP layer for the selected models and contexts."
            if status == "export_complete"
            else "MLP-depth prompt_set_02 readiness has been recorded."
        ),
    }
    json_path = output_dir / "v8_mlp_depth_prompt_set_02_export_inventory.json"
    md_path = output_dir / "v8_mlp_depth_prompt_set_02_export_inventory.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path), "exports": exports}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
