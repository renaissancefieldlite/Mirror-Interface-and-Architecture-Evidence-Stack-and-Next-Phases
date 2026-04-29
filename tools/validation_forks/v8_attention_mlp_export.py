#!/usr/bin/env python3
"""Export real V8 attention-flow and MLP block-delta artifacts.

This script is intentionally an exporter, not a validator. It creates the
missing transformer-internal artifacts required by the locked V8 Attention /
MLP Nest 1 bridge protocol:

- per-layer / per-head top-k attention-flow edges
- per-layer MLP/feed-forward block input/output/delta summaries

It does not create synthetic fallback data. If the local checkpoints cannot be
loaded, the script records readiness only and exits without pretending the gate
has been run.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = (
    ROOT
    / "artifacts"
    / "v8"
    / "residual_stream_bridge"
    / "v8_residual_stream_manifest_2026-04-19.json"
)
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_attention_mlp_exports"
DEFAULT_HF_MODULES_CACHE = (
    Path("/Users/renaissancefieldlite1.0/Documents/Playground")
    / "RICK_NON_PROVISIONAL"
    / "05_activation_mapping"
    / "local_checkpoints"
    / "hf_modules_cache"
)
DEFAULT_HF_HOME = (
    Path("/Users/renaissancefieldlite1.0/Documents/Playground")
    / "RICK_NON_PROVISIONAL"
    / "05_activation_mapping"
    / "local_checkpoints"
    / "hf_home"
)

os.environ.setdefault("HF_MODULES_CACHE", str(DEFAULT_HF_MODULES_CACHE))
os.environ.setdefault("HF_HOME", str(DEFAULT_HF_HOME))
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


ATTENTION_FIELDS = [
    "model",
    "context",
    "layer_index",
    "layer_depth",
    "head_index",
    "query_role",
    "key_rank",
    "key_index",
    "key_region",
    "attention_weight",
    "head_entropy",
    "token_count",
]

MLP_FIELDS = [
    "model",
    "context",
    "layer_index",
    "layer_depth",
    "module_name",
    "input_norm",
    "output_norm",
    "delta_norm",
    "input_output_cosine",
    "token_count",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export V8 attention and MLP artifacts.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="V8 manifest JSON.")
    parser.add_argument("--results-dir", default=str(DEFAULT_OUT), help="Output directory.")
    parser.add_argument("--model", action="append", default=[], help="Display model name. Repeatable.")
    parser.add_argument("--context", action="append", default=[], help="Context label. Defaults to all manifest contexts.")
    parser.add_argument(
        "--checkpoint",
        action="append",
        help="Override checkpoint as DisplayName=/path/to/local/checkpoint. Repeatable.",
    )
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "mps"], help="Torch device.")
    parser.add_argument("--dtype", default="auto", choices=["auto", "float32", "float16", "bfloat16"], help="Torch dtype.")
    parser.add_argument("--max-length", type=int, default=512, help="Maximum prompt tokens for the first export pass.")
    parser.add_argument("--attention-top-k", type=int, default=8, help="Top attention edges per head/query role.")
    parser.add_argument(
        "--layer-scope",
        default="early,middle,late",
        help="Comma-separated layers: early,middle,late,all, or integer layer indexes.",
    )
    parser.add_argument("--check-only", action="store_true", help="Only write checkpoint/readiness inventory.")
    return parser.parse_args()


def resolve_device(choice: str) -> str:
    if choice != "auto":
        return choice
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def resolve_dtype(choice: str) -> Any:
    if choice == "float32":
        return torch.float32
    if choice == "float16":
        return torch.float16
    if choice == "bfloat16":
        return torch.bfloat16
    return "auto"


def checkpoint_overrides(values: list[str] | None) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for value in values or []:
        if "=" not in value:
            raise SystemExit(f"Invalid --checkpoint override: {value!r}; expected DisplayName=/path")
        display, path = value.split("=", 1)
        overrides[display.strip()] = path.strip()
    return overrides


def resolve_checkpoint(model_item: dict[str, Any], overrides: dict[str, str]) -> str | None:
    display = model_item["display_name"]
    env_path = os.environ.get(model_item.get("checkpoint_env", ""))
    candidates = [overrides.get(display), env_path, *model_item.get("checkpoint_candidates", [])]
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate).expanduser()
        if path.exists():
            return str(path.resolve())
    return None


def slug(value: str) -> str:
    return "".join(character.lower() if character.isalnum() else "_" for character in value).strip("_")


def load_model(checkpoint: str, device: str, dtype_choice: str) -> tuple[Any, Any]:
    DEFAULT_HF_MODULES_CACHE.mkdir(parents=True, exist_ok=True)
    DEFAULT_HF_HOME.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(
        checkpoint,
        trust_remote_code=True,
        local_files_only=True,
    )
    if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = resolve_dtype(dtype_choice)
    kwargs: dict[str, Any] = {
        "trust_remote_code": True,
        "local_files_only": True,
    }
    if dtype != "auto":
        kwargs["dtype"] = dtype

    try:
        model = AutoModelForCausalLM.from_pretrained(checkpoint, attn_implementation="eager", **kwargs)
    except TypeError:
        model = AutoModelForCausalLM.from_pretrained(checkpoint, **kwargs)
    model.to(device)
    model.eval()
    if hasattr(model, "config"):
        model.config.output_attentions = True
        model.config.output_hidden_states = False
    return tokenizer, model


def token_span_for_target(tokenizer: Any, prompt: str, target_phrase: str) -> tuple[int, int] | None:
    index = prompt.find(target_phrase)
    if index == -1:
        return None
    prefix = prompt[:index]
    target = prompt[index : index + len(target_phrase)]
    prefix_ids = tokenizer(prefix, add_special_tokens=True, return_tensors="pt")["input_ids"][0]
    target_ids = tokenizer(target, add_special_tokens=False, return_tensors="pt")["input_ids"][0]
    prompt_ids = tokenizer(prompt, return_tensors="pt")["input_ids"][0]
    start = max(0, int(prefix_ids.numel()) - 1)
    end = min(start + int(target_ids.numel()), int(prompt_ids.numel()))
    if end <= start:
        return None
    return start, end


def layer_depth_label(layer_index: int, total_layers: int) -> str:
    if total_layers <= 0:
        return "unknown"
    fraction = (layer_index + 1) / total_layers
    if fraction <= 1 / 3:
        return "early"
    if fraction <= 2 / 3:
        return "middle"
    return "late"


def token_region_label(token_index: int, target_span: tuple[int, int] | None, token_count: int) -> str:
    if token_index < 0:
        return "summary"
    if token_index >= token_count:
        return "padding"
    if not target_span:
        if token_index == token_count - 1:
            return "last_token"
        return "ordinary_token"
    start, end = target_span
    if token_index < start:
        return "pre_anchor"
    if token_index < end:
        return "anchor_phrase"
    if token_index == token_count - 1:
        return "last_token"
    return "post_anchor"


def parse_layer_scope(scope: str, total_layers: int) -> list[int]:
    requested = [item.strip().lower() for item in scope.split(",") if item.strip()]
    if not requested:
        requested = ["early", "middle", "late"]
    selected: set[int] = set()
    for item in requested:
        if item == "all":
            selected.update(range(total_layers))
        elif item == "early":
            selected.add(0)
        elif item == "middle":
            selected.add(max(0, total_layers // 2))
        elif item == "late":
            selected.add(max(0, total_layers - 1))
        elif item.isdigit():
            index = int(item)
            if 0 <= index < total_layers:
                selected.add(index)
        else:
            raise SystemExit(f"Unsupported --layer-scope item: {item!r}")
    return sorted(selected)


def first_tensor(value: Any) -> torch.Tensor | None:
    if isinstance(value, torch.Tensor):
        return value
    if isinstance(value, (list, tuple)):
        for item in value:
            tensor = first_tensor(item)
            if tensor is not None:
                return tensor
    return None


def cosine(a: torch.Tensor, b: torch.Tensor) -> float:
    a_flat = a.reshape(-1).float()
    b_flat = b.reshape(-1).float()
    denom = float(a_flat.norm().item() * b_flat.norm().item())
    if denom == 0.0:
        return 0.0
    return float(torch.dot(a_flat, b_flat).item() / denom)


def module_layer_index(name: str) -> int | None:
    patterns = [
        r"(?:^|\.)layers\.(\d+)\.",
        r"(?:^|\.)h\.(\d+)\.",
        r"(?:^|\.)block\.(\d+)\.",
        r"(?:^|\.)blocks\.(\d+)\.",
        r"(?:^|\.)encoder\.layers\.(\d+)\.",
    ]
    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            return int(match.group(1))
    return None


def discover_mlp_modules(model: Any) -> dict[int, tuple[str, Any]]:
    candidates: dict[int, tuple[str, Any]] = {}
    for name, module in model.named_modules():
        lower = name.lower()
        if not lower:
            continue
        if not (
            lower.endswith(".mlp")
            or lower.endswith(".ffn")
            or lower.endswith(".feed_forward")
            or lower.endswith(".feedforward")
            or "feed_forward" in lower
        ):
            continue
        layer_index = module_layer_index(name)
        if layer_index is None:
            continue
        candidates.setdefault(layer_index, (name, module))
    return candidates


def summarize_mlp_delta(
    model_name: str,
    context_name: str,
    layer_index: int,
    total_layers: int,
    module_name: str,
    hook_input: Any,
    hook_output: Any,
    token_count: int,
) -> dict[str, Any] | None:
    input_tensor = first_tensor(hook_input)
    output_tensor = first_tensor(hook_output)
    if input_tensor is None or output_tensor is None:
        return None
    input_cpu = input_tensor.detach().float().cpu()
    output_cpu = output_tensor.detach().float().cpu()
    if input_cpu.shape != output_cpu.shape:
        return None
    delta = output_cpu - input_cpu
    return {
        "model": model_name,
        "context": context_name,
        "layer_index": layer_index,
        "layer_depth": layer_depth_label(layer_index, total_layers),
        "module_name": module_name,
        "input_norm": round(float(input_cpu.norm().item()), 6),
        "output_norm": round(float(output_cpu.norm().item()), 6),
        "delta_norm": round(float(delta.norm().item()), 6),
        "input_output_cosine": round(cosine(input_cpu, output_cpu), 6),
        "token_count": token_count,
    }


def attention_entropy(weights: torch.Tensor) -> float:
    probs = weights.detach().float().cpu().clamp_min(1e-12)
    entropy = -(probs * probs.log()).sum().item()
    denom = math.log(max(2, int(probs.numel())))
    return float(entropy / denom)


def attention_rows(
    *,
    model_name: str,
    context_name: str,
    attentions: tuple[torch.Tensor, ...],
    selected_layers: list[int],
    target_span: tuple[int, int] | None,
    token_count: int,
    top_k: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    total_layers = len(attentions)
    query_roles: dict[str, list[int]] = {"last_token": [max(0, token_count - 1)]}
    if target_span:
        start, end = target_span
        query_roles["anchor_phrase"] = list(range(start, min(end, token_count)))

    for layer_index in selected_layers:
        if layer_index >= len(attentions):
            continue
        layer_attention = attentions[layer_index]
        if layer_attention is None:
            continue
        attn = layer_attention.detach().float().cpu()
        if attn.ndim != 4:
            continue
        attn = attn[0]
        head_count = int(attn.shape[0])
        for head_index in range(head_count):
            head_matrix = attn[head_index]
            for query_role, query_indices in query_roles.items():
                valid_queries = [idx for idx in query_indices if 0 <= idx < head_matrix.shape[0]]
                if not valid_queries:
                    continue
                weights = head_matrix[valid_queries].mean(dim=0)
                k = min(top_k, int(weights.numel()))
                top_values, top_indices = torch.topk(weights, k=k)
                entropy = attention_entropy(weights)
                for rank, (value, key_index) in enumerate(zip(top_values, top_indices), start=1):
                    key_idx = int(key_index.item())
                    rows.append(
                        {
                            "model": model_name,
                            "context": context_name,
                            "layer_index": layer_index,
                            "layer_depth": layer_depth_label(layer_index, total_layers),
                            "head_index": head_index,
                            "query_role": query_role,
                            "key_rank": rank,
                            "key_index": key_idx,
                            "key_region": token_region_label(key_idx, target_span, token_count),
                            "attention_weight": round(float(value.item()), 8),
                            "head_entropy": round(entropy, 8),
                            "token_count": token_count,
                        }
                    )
    return rows


def select_models(manifest: dict[str, Any], selected_names: set[str]) -> list[dict[str, Any]]:
    models = manifest.get("models", [])
    if not selected_names:
        return models
    return [model for model in models if model.get("display_name") in selected_names]


def selected_contexts(model_item: dict[str, Any], selected_names: set[str]) -> list[dict[str, Any]]:
    contexts = model_item.get("contexts", [])
    if not selected_names:
        return contexts
    return [context for context in contexts if context.get("context") in selected_names]


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


def write_markdown_report(report: dict[str, Any], path: Path) -> None:
    if report["status"] == "export_complete":
        status_lines = [
            "Current status is export complete: the CSV insertion point now exists.",
            "The next evidence question is validation: whether those rows separate",
            "lattice/mirror from neutral/technical above shuffled controls and graph",
            "baselines.",
        ]
    else:
        status_lines = [
            "Current status is readiness only: the selected checkpoints are available,",
            "but the full attention/MLP CSV export and validation controls still need",
            "to run.",
        ]
    lines = [
        "# V8 Attention / MLP Export Gate",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Purpose",
        "",
        "This is the live handoff from V8 hidden-state evidence into the actual",
        "transformer mechanics.",
        "",
        "V8 already tells us where the representation lands in the residual stream.",
        "This gate is for the next question: how the model routes tokens through",
        "attention heads, and how the MLP/feed-forward blocks rewrite the",
        "representation after routing.",
        "",
        "The export produces the real internal objects needed for the next Nest 1",
        "closeout:",
        "",
        "- attention top-k token-routing edges for `GRAPH-2C`",
        "- attention head entropy / routing summaries for `INFO-1` and `SPEC-1`",
        "- MLP block input/output/delta rows for `TENSOR`, `GEO`, `DYN`, and `OPT`",
        "",
        *status_lines,
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
        lines.extend(["", "## Exported Files", ""])
        for key, value in report["exports"].items():
            lines.append(f"- {key}: `{value}`")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- `check_only_ready` means the local checkpoints and manifest are ready, not that attention/MLP evidence has been collected.",
            "- `export_complete` means CSV artifacts were written and can be passed into GRAPH-2C / MLP validation.",
            "- If a model cannot return attentions or expose MLP modules, that is recorded as a model-interface blocker.",
            "- Residual-stream evidence and attention/MLP evidence are connected, but they are not interchangeable.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_exports(args: argparse.Namespace, manifest: dict[str, Any], selected_models: set[str], selected_context_names: set[str], overrides: dict[str, str]) -> dict[str, str]:
    results_dir = Path(args.results_dir).resolve()
    attention_path = results_dir / "v8_attention_topk_edges.csv"
    mlp_path = results_dir / "v8_mlp_block_deltas.csv"
    attention_rows_written = 0
    mlp_rows_written = 0
    device = resolve_device(args.device)

    with attention_path.open("w", encoding="utf-8", newline="") as attention_handle, mlp_path.open("w", encoding="utf-8", newline="") as mlp_handle:
        attention_writer = csv.DictWriter(attention_handle, fieldnames=ATTENTION_FIELDS)
        mlp_writer = csv.DictWriter(mlp_handle, fieldnames=MLP_FIELDS)
        attention_writer.writeheader()
        mlp_writer.writeheader()

        for model_item in select_models(manifest, selected_models):
            checkpoint = resolve_checkpoint(model_item, overrides)
            if checkpoint is None:
                continue
            tokenizer, model = load_model(checkpoint, device=device, dtype_choice=args.dtype)
            contexts = selected_contexts(model_item, selected_context_names)
            mlp_modules = discover_mlp_modules(model)

            for context in contexts:
                prompt = context["prompt"]
                encoded = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=args.max_length)
                input_ids = encoded["input_ids"].to(device)
                attention_mask = encoded.get("attention_mask")
                if attention_mask is not None:
                    attention_mask = attention_mask.to(device)
                token_count = int(input_ids.shape[-1])
                target_span = token_span_for_target(tokenizer, prompt, context["target_phrase"])

                selected_layers: list[int] | None = None
                captured_mlp: dict[int, tuple[str, Any, Any]] = {}
                hook_handles = []

                def make_hook(layer_index: int, module_name: str):
                    def hook(_module: Any, hook_input: Any, hook_output: Any) -> None:
                        captured_mlp[layer_index] = (module_name, hook_input, hook_output)

                    return hook

                with torch.no_grad():
                    outputs = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        output_attentions=True,
                        output_hidden_states=False,
                        use_cache=False,
                    )
                attentions = tuple(outputs.attentions or ())
                selected_layers = parse_layer_scope(args.layer_scope, len(attentions))

                for layer_index in selected_layers:
                    module_pair = mlp_modules.get(layer_index)
                    if module_pair is None:
                        continue
                    module_name, module = module_pair
                    hook_handles.append(module.register_forward_hook(make_hook(layer_index, module_name)))

                if hook_handles:
                    with torch.no_grad():
                        model(
                            input_ids=input_ids,
                            attention_mask=attention_mask,
                            output_attentions=False,
                            output_hidden_states=False,
                            use_cache=False,
                        )
                    for handle in hook_handles:
                        handle.remove()

                for row in attention_rows(
                    model_name=model_item["display_name"],
                    context_name=context["context"],
                    attentions=attentions,
                    selected_layers=selected_layers,
                    target_span=target_span,
                    token_count=token_count,
                    top_k=args.attention_top_k,
                ):
                    attention_writer.writerow(row)
                    attention_rows_written += 1

                for layer_index, (module_name, hook_input, hook_output) in sorted(captured_mlp.items()):
                    row = summarize_mlp_delta(
                        model_name=model_item["display_name"],
                        context_name=context["context"],
                        layer_index=layer_index,
                        total_layers=len(attentions),
                        module_name=module_name,
                        hook_input=hook_input,
                        hook_output=hook_output,
                        token_count=token_count,
                    )
                    if row is None:
                        continue
                    mlp_writer.writerow(row)
                    mlp_rows_written += 1

            del model
            del tokenizer

    return {
        "attention_edges_csv": str(attention_path),
        "mlp_deltas_csv": str(mlp_path),
        "attention_rows": str(attention_rows_written),
        "mlp_rows": str(mlp_rows_written),
    }


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    results_dir = Path(args.results_dir).resolve()
    results_dir.mkdir(parents=True, exist_ok=True)
    selected_models = set(args.model)
    selected_context_names = set(args.context)
    overrides = checkpoint_overrides(args.checkpoint)
    device = resolve_device(args.device)

    inventory = readiness_inventory(manifest, selected_models, overrides, selected_context_names)
    ready_count = sum(1 for item in inventory if item["checkpoint_status"] == "ready")
    status = "check_only_ready" if ready_count == len(inventory) and inventory else "check_only_blocked"
    exports: dict[str, str] = {}

    if not args.check_only:
        exports = run_exports(args, manifest, selected_models, selected_context_names, overrides)
        status = "export_complete" if int(exports["attention_rows"]) > 0 or int(exports["mlp_rows"]) > 0 else "export_empty"

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "manifest": str(manifest_path),
        "selected_models": sorted(selected_models),
        "selected_contexts": sorted(selected_context_names),
        "device": device,
        "dtype": args.dtype,
        "max_length": args.max_length,
        "layer_scope": args.layer_scope,
        "inventory": inventory,
        "exports": exports,
    }
    json_path = results_dir / "v8_attention_mlp_export_inventory.json"
    md_path = results_dir / "v8_attention_mlp_export_inventory.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown_report(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
