# V8 Attention / MLP Export Gate

Status: `check_only_ready`

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

Current status is readiness only: the selected checkpoints are available,
but the full attention/MLP CSV export and validation controls still need
to run.

## Scope

- manifest: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/v8_residual_stream_manifest_2026-04-19.json`
- selected models: `all`
- selected contexts: `all`
- device: `cpu`
- max length: `512`

## Inventory

| Model | Checkpoint status | Contexts |
| --- | --- | --- |
| Gemma | `ready` | lattice, neutral, technical |
| Mistral | `ready` | lattice, neutral, technical |
| Qwen | `ready` | lattice, neutral, technical |
| DeepSeek | `ready` | lattice, neutral, technical |
| Hermes | `ready` | lattice, neutral, technical |
| Nemotron | `ready` | lattice, neutral, technical |
| GLM | `ready` | lattice, neutral, technical |
| SmolLM3 | `ready` | lattice, neutral, technical |

## Boundary

- `check_only_ready` means the local checkpoints and manifest are ready, not that attention/MLP evidence has been collected.
- `export_complete` means CSV artifacts were written and can be passed into GRAPH-2C / MLP validation.
- If a model cannot return attentions or expose MLP modules, that is recorded as a model-interface blocker.
- Residual-stream evidence and attention/MLP evidence are connected, but they are not interchangeable.
