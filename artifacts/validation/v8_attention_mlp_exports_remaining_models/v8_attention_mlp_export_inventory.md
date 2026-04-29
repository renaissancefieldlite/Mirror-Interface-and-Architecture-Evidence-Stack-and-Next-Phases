# V8 Attention / MLP Export Gate

Status: `export_complete`

## Purpose

This is the live handoff from V8 hidden-state evidence into the actual
transformer mechanics.

V8 already tells us where the representation lands in the residual stream.
This gate is for the next question: how the model routes tokens through
attention heads, and how the MLP/feed-forward blocks rewrite the
representation after routing.

The export produces the real internal objects needed for the next Nest 1
closeout:

- attention top-k token-routing edges for `GRAPH-2C`
- attention head entropy / routing summaries for `INFO-1` and `SPEC-1`
- MLP block input/output/delta rows for `TENSOR`, `GEO`, `DYN`, and `OPT`

Current status is export complete: the CSV insertion point now exists.
The next evidence question is validation: whether those rows separate
lattice/mirror from neutral/technical above shuffled controls and graph
baselines.

## Scope

- manifest: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/v8_residual_stream_manifest_2026-04-19.json`
- selected models: `DeepSeek, Gemma, Mistral, Nemotron, Qwen, SmolLM3`
- selected contexts: `all`
- device: `cpu`
- max length: `384`

## Inventory

| Model | Checkpoint status | Contexts |
| --- | --- | --- |
| Gemma | `ready` | lattice, neutral, technical |
| Mistral | `ready` | lattice, neutral, technical |
| Qwen | `ready` | lattice, neutral, technical |
| DeepSeek | `ready` | lattice, neutral, technical |
| Nemotron | `ready` | lattice, neutral, technical |
| SmolLM3 | `ready` | lattice, neutral, technical |

## Exported Files

- attention_edges_csv: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/v8_attention_mlp_exports_remaining_models/v8_attention_topk_edges.csv`
- mlp_deltas_csv: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/v8_attention_mlp_exports_remaining_models/v8_mlp_block_deltas.csv`
- attention_rows: `14400`
- mlp_rows: `45`

## Boundary

- `check_only_ready` means the local checkpoints and manifest are ready, not that attention/MLP evidence has been collected.
- `export_complete` means CSV artifacts were written and can be passed into GRAPH-2C / MLP validation.
- If a model cannot return attentions or expose MLP modules, that is recorded as a model-interface blocker.
- Residual-stream evidence and attention/MLP evidence are connected, but they are not interchangeable.
