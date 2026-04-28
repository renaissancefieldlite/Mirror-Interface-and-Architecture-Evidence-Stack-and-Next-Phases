# V8 Attention / MLP Export Inventory

Status: `check_only_ready`

## Purpose

This artifact records whether the transformer-internal attention and MLP
export gate is ready. It does not treat hidden-state residual traces as
attention or MLP evidence.

## Scope

- manifest: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/v8_residual_stream_manifest_2026-04-19.json`
- selected models: `GLM, Hermes`
- selected contexts: `all`
- device: `cpu`
- max length: `512`

## Inventory

| Model | Checkpoint status | Contexts |
| --- | --- | --- |
| Hermes | `ready` | lattice, neutral, technical |
| GLM | `ready` | lattice, neutral, technical |

## Boundary

- `check_only_ready` means the local checkpoints and manifest are ready, not that attention/MLP evidence has been collected.
- `export_complete` means CSV artifacts were written and can be passed into GRAPH-2C / MLP validation.
- If a model cannot return attentions or expose MLP modules, that is recorded as a model-interface blocker.
