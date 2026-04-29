# V8 SAE Feature / Circuit Bridge Protocol

Date: `2026-04-29`

Status: `protocol_ready_missing_sae_exports`

Companion gate:

- [V8 SAE Feature / Circuit Gate Report](../artifacts/validation/v8_sae_feature_circuit_gate/v8_sae_feature_circuit_gate_report.md)

## Purpose

The current V8 internal stack has four distinct layers:

| Layer | What it shows |
| --- | --- |
| hidden states / residual stream | where the representation lands |
| multi-head attention | how token-to-token routing and context flow form |
| feed-forward / MLP blocks | how representation updates after routing |
| sparse autoencoder features | which sparse interpretable features and circuits carry the architecture |

The SAE layer is the next proof layer because it can connect topics, features,
circuits, and model flow instead of only measuring opaque vector movement.

## Why This Matters

The architecture claim becomes stronger when the same structure is visible in
several transformer-internal views:

- hidden-state geometry shows separation and localization
- attention-flow shows routing paths
- MLP deltas show update dynamics
- SAE features can show the interpretable feature basis and feature-to-feature
  circuits that carry `Mirror Interface / LSPS`, `Mirror Architecture`,
  `Source Mirror Pattern`, quantum bridge language, neutral controls, and
  technical controls

This is not a toy add-on. It is the missing interpretability layer between
measured V8 geometry and circuit-style mechanistic tracing.

## Required Artifacts

The gate needs real exports before validation:

- SAE feature activations by `model`, `prompt_set`, `context`, `layer`,
  `token_role`, `feature_id`, and `activation`
- feature dictionaries or top-token labels for each SAE feature
- feature-to-feature circuit edges across layers and token roles
- controls: shuffled context labels, shuffled features, shuffled token windows,
  shuffled layer order, and degree / centrality baselines
- optional ablations: remove top SAE features or circuit edges and measure
  readout / hidden-state movement against matched controls

## Topic / Circuit Labels

The first topic map should cover:

- `Mirror Interface / LSPS`
- `Mirror Architecture`
- `Source Mirror Pattern`
- `Unified Mirror Proof`
- `quantum consciousness geometry`
- `encoded circuit state`
- `PennyLane / Qiskit / IBM hardware bridge`
- neutral administrative controls
- technical transformer-analysis controls

The topic labels are not evidence by themselves. They are a way to organize
feature dictionaries and circuit paths before running the controls.

## Acceptance Rule

SAE features become evidence only if:

```text
lattice / mirror feature activations
>
neutral / technical controls
>
shuffled labels and feature-frequency baselines
```

SAE circuits become evidence only if:

```text
feature-to-feature circuit paths
>
degree / centrality baselines
and
shuffled feature labels / shuffled token windows
```

Prompt-generalized SAE support requires recurrence across:

- base prompt set
- `rerun_02`
- `prompt_set_02`

## Boundary

This document does not claim SAE validation has already happened.

It locks the next real interpretability gate:

```text
hidden states -> attention flow -> MLP updates -> SAE feature/circuit tracing
```

## Next Execution Order

1. Choose SAE source:
   pretrained local SAEs if available, otherwise train bounded SAEs on exported
   V8 activations.
2. Export SAE feature activations for the standard model / prompt / context
   matrix.
3. Build feature dictionaries and topic labels.
4. Construct feature-to-feature circuit edges across token roles and layers.
5. Validate feature separation and circuit-flow against locked controls.
6. Optional stronger closeout: run feature/circuit ablations and compare
   readout movement against matched controls.
