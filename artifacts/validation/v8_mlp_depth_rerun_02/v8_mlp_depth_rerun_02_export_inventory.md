# V8 MLP Depth rerun_02 Export

Status: `export_complete`

## Clean Read

MLP-depth rerun_02 export is complete. This artifact expands the feed-forward gate from the earlier early/middle/late sample into every available MLP layer for the selected models and contexts.

## Scope

- manifest: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/v8_residual_stream_manifest_2026-04-19.json`
- set name: `rerun_02`
- selected models: `Gemma, Mistral, Qwen, DeepSeek, Hermes, Nemotron, GLM, SmolLM3`
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
| Hermes | `ready` | lattice, neutral, technical |
| Nemotron | `ready` | lattice, neutral, technical |
| GLM | `ready` | lattice, neutral, technical |
| SmolLM3 | `ready` | lattice, neutral, technical |

## Exported Rows

| Model | MLP modules | Contexts | Rows |
| --- | ---: | ---: | ---: |
| Gemma | `42` | `3` | `126` |
| Mistral | `32` | `3` | `96` |
| Qwen | `36` | `3` | `108` |
| DeepSeek | `28` | `3` | `84` |
| Hermes | `32` | `3` | `96` |
| Nemotron | `0` | `3` | `0` |
| GLM | `40` | `3` | `120` |
| SmolLM3 | `36` | `3` | `108` |

- MLP depth CSV: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/v8_mlp_depth_rerun_02/v8_mlp_depth_rerun_02.csv`
- total rows: `738`
