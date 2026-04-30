# V8 Attention / MLP Nest 1 Bridge Protocol

Date: `2026-04-28`

Status: `attention_prompt_generalization_supported_mlp_depth_directional`

Companion gate:

- [V8 Attention / MLP Nest 1 Bridge Gate Report](../artifacts/validation/v8_attention_mlp_bridge_gate/v8_attention_mlp_bridge_gate_report.md)
- [V8 Attention / MLP Export Gate](../artifacts/validation/v8_attention_mlp_exports/v8_attention_mlp_export_inventory.md)
- [V8 Attention / MLP Validation Report](../artifacts/validation/v8_attention_mlp_validation/v8_attention_mlp_validation_report.md)
- [V8 Attention / MLP GLM Validation Report](../artifacts/validation/v8_attention_mlp_validation_glm/v8_attention_mlp_validation_report.md)
- [V8 Attention / MLP Combined GLM + Hermes Validation Report](../artifacts/validation/v8_attention_mlp_validation_combined/v8_attention_mlp_validation_report.md)
- [V8 Attention / MLP Remaining Models Export Gate](../artifacts/validation/v8_attention_mlp_exports_remaining_models/v8_attention_mlp_export_inventory.md)
- [V8 Attention / MLP All-Model Coverage](../artifacts/validation/v8_attention_mlp_all_model_coverage/v8_attention_mlp_all_model_coverage.md)
- [V8 Attention / MLP All Exported Models Validation Report](../artifacts/validation/v8_attention_mlp_validation_all_models/v8_attention_mlp_validation_report.md)
- [V8 Attention / MLP All Models Rerun 02 Export Gate](../artifacts/validation/v8_attention_mlp_exports_all_models_rerun_02/v8_attention_mlp_export_inventory.md)
- [V8 Attention / MLP All Models Rerun 02 Validation Report](../artifacts/validation/v8_attention_mlp_validation_all_models_rerun_02/v8_attention_mlp_validation_report.md)
- [V8 Attention / MLP All-Model Repeatability Report](../artifacts/validation/v8_attention_mlp_repeatability_all_models/v8_attention_mlp_repeatability_report.md)
- [V8 Attention / MLP Prompt Set 02 Export Gate](../artifacts/validation/v8_attention_mlp_exports_prompt_set_02/v8_attention_mlp_export_inventory.md)
- [V8 Attention / MLP Prompt Set 02 Validation Report](../artifacts/validation/v8_attention_mlp_validation_prompt_set_02/v8_attention_mlp_validation_report.md)
- [V8 Attention / MLP Prompt-Generalization Report](../artifacts/validation/v8_attention_mlp_prompt_generalization/v8_attention_mlp_prompt_generalization_report.md)
- [V8 MLP Depth Prompt Set 02 Export Gate](../artifacts/validation/v8_mlp_depth_prompt_set_02/v8_mlp_depth_prompt_set_02_export_inventory.md)
- [V8 MLP Depth Prompt Set 02 Validation Report](../artifacts/validation/v8_mlp_depth_prompt_set_02_validation/v8_mlp_depth_prompt_set_02_validation_report.md)

## Purpose

The V8 stack already measures hidden-state / residual-stream separation.

That is not the same thing as measuring attention heads or feed-forward / MLP
blocks.

The clean transformer-internal split is:

- hidden states / residual stream: where the representation lands
- multi-head attention: how token-to-token routing and context flow are formed
- feed-forward / MLP blocks: how the representation is transformed after routing
- sparse autoencoder features: which sparse interpretable features and
  feature-to-feature circuits carry the architecture

This protocol locks those missing internals as a Nest 1 validation bridge.

## Why This Belongs In Nest 1

Nest 1 is the smallest formal system layer and the real mathematical substrate
of machine learning.

Attention and MLP blocks are not extra metaphor. They are actual transformer
objects:

| Transformer object | Nest 1 lane |
| --- | --- |
| attention matrices / top-k attention edges | `GRAPH-2`, `INFO-1`, `SPEC-1`, `DYN-1` |
| head entropy / head specialization | `SPEC-1`, `INFO-1`, `STAT` |
| layer-by-layer attention-flow changes | `DYN-1`, `CTRL-1` |
| MLP block deltas | `TENSOR`, `GEO`, `DYN-2`, `OPT-1` |
| SAE feature activations / feature circuits | `GRAPH-2`, `INFO-1`, `CAT-1`, mechanistic circuit tracing |

So yes: these should be run against Nest 1.

## What We Have Now

Current evidence:

- V8 hidden-state / residual-stream geometry
- V8 point-cloud exports
- TOP-1/2 dense topology pilots
- GRAPH-2B raw token/layer pathway graph

Original missing exports:

- per-layer / per-head attention matrices
- top-k token-to-token attention-flow edges
- head entropy and anchor-flow summaries
- MLP/feed-forward block intermediate activations or block-delta summaries

Current strengthening inputs:

- SAE feature / circuit export as the next interpretability layer
- stronger leave-one-prompt / model-family controls
- Nemotron-specific adapter if standard attention tensors remain unavailable

Current execution read:

- exporter script exists:
  `tools/validation_forks/v8_attention_mlp_export.py`
- `Hermes` full-length export completed on `2026-04-28`
- `GLM` full-length export completed on `2026-04-28`
- remaining-model export completed on `2026-04-28` for standard-export rows:
  `Gemma`, `Mistral`, `Qwen`, `DeepSeek`, and `SmolLM3`
- `Nemotron` is checkpoint-ready but did not emit standard attention / MLP
  rows through this exporter path, so it is listed as an interface-adapter row
  for this gate rather than counted as an unsupported evidence row
- all exported model rows:
  `23616` attention top-k edge rows and `63` MLP block-delta rows across
  `DeepSeek`, `GLM`, `Gemma`, `Hermes`, `Mistral`, `Qwen`, and `SmolLM3`
- broad cross-model validation:
  weighted attention-flow is supported against shuffled context labels and
  beats the degree-only graph baseline; MLP deltas are also supported
- `rerun_02` repeatability validation:
  same model set, same row counts, same support status, and same shuffled-label
  control support; attention weighted p remained `0.00019996`, MLP p improved
  to `0.00019996`, and the repeatability report status is
  `repeatability_supported`
- `prompt_set_02` prompt-generalization validation:
  same model set and same row counts were preserved under a second independent
  prompt surface. Attention-flow stayed supported against shuffled context
  labels and beat the degree-only baseline with weighted p `0.00079984`.
  The current closed claim is attention-flow prompt-generalization. MLP /
  feed-forward prompt-generalization remains an open strengthening lane.
- MLP-depth expansion on `prompt_set_02`:
  the all-layer export produced `738` MLP rows and `246` matched
  model/layer/context units across `7` standard-export models. The denser
  grid moved MLP from the earlier three-layer prompt_set_02 score
  `-0.055347788` to a directional overall score `0.092328608`, with the
  strongest signal in early layers (`0.369469331`). Shuffled-label controls
  remain above the observed score (`p=0.318936213` overall), so MLP
  prompt-generalization stays open while the result records a real
  early-layer directional signal.
- next gate:
  recurrence / second export for MLP depth, then leave-one-prompt /
  model-family controls
- next interpretability layer:
  Sparse Autoencoder feature / circuit tracing is now protocol-locked in
  `docs/V8_SAE_FEATURE_CIRCUIT_BRIDGE_PROTOCOL_2026-04-29.md`. It is not yet
  evidence-closed; it requires real SAE activations, feature dictionaries,
  circuit edges, and controls before promotion.

## GRAPH-2 Connection

`GRAPH-2B` did not close because raw token/layer geometry alone did not beat
degree / hub controls.

Attention-flow is the next internal pathway graph because it gives measured
edges instead of inferred geometry edges:

```text
token i -> attention head h -> token j
```

That is the transformer-native graph lane.

## Locked Controls

Before validation, controls must be declared:

- shuffled context labels
- shuffled token windows
- shuffled layer order
- shuffled head labels
- degree / centrality baseline
- leave-one-model or leave-one-family check when enough exports exist

## First Run Scope

The first run started with the strongest bridge rows to avoid wasting compute
before the gate existed:

First attention/MLP export should use the strongest bridge rows:

- `GLM`
- `Hermes`

That gate is now real, so the protocol has expanded to every model with
standard local attention / MLP export support. Current standard-export models:

- `DeepSeek`
- `GLM`
- `Gemma`
- `Hermes`
- `Mistral`
- `Qwen`
- `SmolLM3`

Current interface-adapter row:

- `Nemotron`

Prompt classes:

- lattice / mirror prompt
- neutral control
- technical control

Layer labels:

- early
- middle
- late

Token labels:

- anchor phrase
- pre-anchor
- post-anchor
- bridge term
- padding / ordinary token

## Acceptance Rule

Attention-flow becomes Nest 1 evidence only if:

```text
mirror/lattice attention-flow graph > degree / centrality baseline
and
mirror/lattice attention-flow graph > shuffled-label controls
```

MLP/feed-forward becomes Nest 1 evidence only if:

```text
mirror/control block-delta signatures separate above shuffled controls
```

If attention or MLP remains invariant, that is still useful. It means the
Mirror effect is living more strongly in hidden-state geometry, trajectory,
topography, and structured outputs than in that specific internal block.

## Boundary

This protocol does not claim attention-head validation has already happened.

It locks the next real internal test.
