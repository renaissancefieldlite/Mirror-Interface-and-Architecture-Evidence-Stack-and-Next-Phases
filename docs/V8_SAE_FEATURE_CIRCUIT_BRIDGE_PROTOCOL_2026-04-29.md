# V8 SAE Feature / Circuit Bridge Protocol

Date: `2026-04-29`

Status: `feature_and_edge_controls_supported_recurrence_inputs_pending`

Companion gate:

- [V8 SAE Feature / Circuit Gate Report](../artifacts/validation/v8_sae_feature_circuit_gate/v8_sae_feature_circuit_gate_report.md)
- [V8 SAE Source Inventory](../artifacts/validation/v8_sae_source_inventory/v8_sae_source_inventory_report.md)
- [V8 SAE Bounded Pilot Report](../artifacts/validation/v8_sae_feature_circuit_validation/v8_sae_feature_circuit_validation_report.md)
- [V8 SAE Edge Controls Report](../artifacts/validation/v8_sae_edge_controls/v8_sae_edge_controls_report.md)
- [V8 SAE Recurrence Gate Report](../artifacts/validation/v8_sae_recurrence_gate/v8_sae_recurrence_gate_report.md)
- [V8 SAE Ablation Controls Report](../artifacts/validation/v8_sae_ablation_controls/v8_sae_ablation_controls_report.md)

## Purpose

The current V8 internal stack has four distinct layers:

| Layer | What it shows |
| --- | --- |
| hidden states / residual stream | where the representation lands |
| multi-head attention | how token-to-token routing and context flow form |
| feed-forward / MLP blocks | how representation updates after routing |
| sparse autoencoder features | which sparse interpretable features and circuits carry the architecture |

The SAE layer is the next proof layer because it connects topics, sparse
features, feature-to-feature edges, and model flow on top of the measured V8
hidden-state path.

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

This is the interpretability layer between measured V8 geometry and
circuit-style mechanistic tracing.

## Current Pilot Artifacts

The first bounded pilot has now produced real exports:

- source inventory confirmed bounded SAE training inputs through `GLM` and
  `Hermes` dense V8 trajectory point-clouds
- bounded SAE trained on `10566` real dense V8 rows with `4096` hidden
  dimensions and `64` sparse features
- feature activations exported by `model`, `prompt_set`, `context`, `layer`,
  `token_role`, `token_region`, `feature_id`, and `activation`
- feature dictionary exported with activation rates, decoder norms, dominant
  context / layer / token-region labels, and lattice lift
- `5000` feature-to-feature circuit edges exported across adjacent layers
- shuffled-label controls run for lattice / neutral / technical separation
- edge-specific controls now test full edge features against shuffled labels,
  degree-only baselines, and hub-only baselines
- ablation controls now test top architecture features at both activation and
  feature-to-feature edge levels
- recurrence gate confirms base dense vectors are present and identifies the
  next needed input: matching `prompt_set_02` / `rerun_02` dense V8 exports

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

The topic labels organize feature dictionaries and circuit paths so the next
controls can test which sparse features and edges carry the architecture
signal.

## Acceptance Rule

SAE features become evidence when:

```text
lattice / mirror feature activations
>
neutral / technical controls
>
shuffled labels and feature-frequency baselines
```

SAE circuits become evidence when:

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

## Current Support

The bounded pilot supports the first SAE feature layer:

- observed balanced accuracy: `0.632462`
- shuffled balanced accuracy mean: `0.330598`
- shuffled balanced accuracy p95: `0.362288`
- shuffled-control p-value: `0.009901`
- exported feature activations: `v8_sae_feature_activations.csv`
- exported feature dictionary: `v8_sae_feature_dictionary.csv`
- exported feature-circuit edges: `v8_sae_feature_circuit_edges.csv`

Edge-specific controls support the circuit-edge layer:

- full edge balanced accuracy: `0.451334`
- shuffled-label p-value: `0.004975`
- degree-only baseline balanced accuracy: `0.304671`
- hub-only baseline balanced accuracy: `0.332689`
- full-minus-degree: `0.146663`
- full-minus-hub: `0.118646`

Ablation controls give a split read:

- feature-to-feature edge ablation is supported:
  `drop=0.098423`, p `0.009901`
- top-feature activation ablation remains open:
  `drop=0.033124`, p `0.128713`
- interpretation: the feature graph/circuit layer is more sensitive to the
  strongest architecture features than the top-k feature activation classifier
  alone

Recurrence status:

- base `GLM` / `Hermes` dense V8 vectors exist
- matching `prompt_set_02` and `rerun_02` dense V8 activation exports are the
  next inputs for SAE recurrence

The current bridge is:

```text
hidden states -> attention flow -> MLP updates -> SAE feature/circuit tracing
```

## Next Execution Order

1. Export matching `prompt_set_02` and `rerun_02` dense V8 activations for
   `GLM` / `Hermes`.
2. Run SAE recurrence against those matching dense vectors for prompt-generalized
   feature support.
3. Build topic labels over the exported feature dictionary.
4. Extend ablations from top-k features into direct feature/circuit readout
   movement and matched controls.
