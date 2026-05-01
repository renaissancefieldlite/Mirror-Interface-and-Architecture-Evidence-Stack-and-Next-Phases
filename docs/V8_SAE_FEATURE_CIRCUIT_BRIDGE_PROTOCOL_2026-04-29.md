# V8 SAE Feature / Circuit Bridge Protocol

Date: `2026-04-29`

Status: `feature_edge_recurrence_supported_recurrent_ablation_partial`

Companion gate:

- [V8 SAE Feature / Circuit Gate Report](../artifacts/validation/v8_sae_feature_circuit_gate/v8_sae_feature_circuit_gate_report.md)
- [V8 SAE Source Inventory](../artifacts/validation/v8_sae_source_inventory/v8_sae_source_inventory_report.md)
- [V8 SAE Bounded Pilot Report](../artifacts/validation/v8_sae_feature_circuit_validation/v8_sae_feature_circuit_validation_report.md)
- [V8 SAE Edge Controls Report](../artifacts/validation/v8_sae_edge_controls/v8_sae_edge_controls_report.md)
- [V8 SAE Recurrence Gate Report](../artifacts/validation/v8_sae_recurrence_gate/v8_sae_recurrence_gate_report.md)
- [V8 SAE Ablation Controls Report](../artifacts/validation/v8_sae_ablation_controls/v8_sae_ablation_controls_report.md)
- [V8 SAE Recurrence Validation Report](../artifacts/validation/v8_sae_recurrence_validation/v8_sae_recurrence_validation_report.md)
- [V8 SAE Gemma Recurrence Validation Report](../artifacts/validation/v8_sae_gemma_recurrence_validation/v8_sae_gemma_recurrence_validation_report.md)
- [V8 SAE Feature-Edge Recurrence Report](../artifacts/validation/v8_sae_feature_edge_recurrence/v8_sae_feature_edge_recurrence_report.md)
- [V8 SAE Recurrent Branch Ablation Report](../artifacts/validation/v8_sae_recurrent_branch_ablation/v8_sae_recurrent_branch_ablation_report.md)

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
- recurrence validation now applies the locked bounded SAE encoder across
  base, `rerun_02`, and `prompt_set_02` dense V8 exports
- Gemma is now carried as a model-native third SAE branch: Gemma dense vectors
  use hidden size `2560`, so the branch trains a Gemma-native SAE on Gemma base
  and applies that locked encoder to Gemma `rerun_02` and `prompt_set_02`
- feature-edge recurrence now regenerates adjacent-layer feature-to-feature
  edges across base, `rerun_02`, and `prompt_set_02` for both branches
- recurrent-branch ablation now removes shared recurrent endpoint features and
  exact recurrent edge keys to test whether the measured feature/circuit paths
  move transfer readout beyond matched random removals

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

- base, `rerun_02`, and `prompt_set_02` `GLM` / `Hermes` dense V8 vectors exist
- within-set feature separation is supported across all three dense exports:
  base `0.619617213`, rerun_02 `0.641035294`, prompt_set_02 `0.495413961`,
  each with p `0.00990099`
- base-trained SAE transfer is supported into rerun_02 (`0.629265629`) and
  prompt_set_02 (`0.45959596`), each with p `0.00990099`
- feature-lift recurrence is strongest on rerun_02 (cosine `0.9963938`,
  top-feature Jaccard `0.818181818`) and remains present under prompt_set_02
  (cosine `0.779671907`, top-feature Jaccard `0.333333333`)

Gemma-native recurrence status:

- Gemma base, `rerun_02`, and `prompt_set_02` dense V8 vectors now exist with
  hidden size `2560`
- a Gemma-native SAE trained on `5355` real Gemma base dense rows and `64`
  sparse features
- within-set feature separation is supported across all three Gemma dense
  exports: base `0.479140512`, rerun_02 `0.493431208`, prompt_set_02
  `0.418165016`, each with p `0.00990099`
- base-trained Gemma SAE transfer is supported into rerun_02 (`0.510737628`)
  and prompt_set_02 (`0.389542484`), each with p `0.00990099`
- feature-lift recurrence is very strong on rerun_02 (cosine `0.967395663`,
  top-feature Jaccard `0.538461538`) and remains present under prompt_set_02
  (cosine `0.392933488`, top-feature Jaccard `0.176470588`)

Feature-edge recurrence status:

- GLM/Hermes edge recurrence closes cleanly:
  within-set edge separation is supported for base (`0.455882927`), rerun_02
  (`0.464051642`), and prompt_set_02 (`0.376823065`), each with p
  `0.00990099`
- GLM/Hermes base-trained edge transfer is supported into rerun_02
  (`0.52387397`) and prompt_set_02 (`0.395827668`), each with p
  `0.00990099`
- Gemma edge recurrence is split:
  within-set Gemma edge separation remains open, while base-trained Gemma edge
  transfer is supported into rerun_02 (`0.438121048`) and prompt_set_02
  (`0.367434508`), each with p `0.00990099`
- weighted edge-signature recurrence is strong on rerun_02 for both branches:
  GLM/Hermes cosine `0.768127447`, Gemma cosine `0.803169721`; prompt_set_02
  remains present but lower: GLM/Hermes cosine `0.391837556`, Gemma cosine
  `0.528171679`

Recurrent-branch ablation status:

- GLM/Hermes base -> rerun_02 supports endpoint-feature ablation
  (`drop=0.090389435`, p `0.00990099`) and exact edge-key ablation
  (`drop=0.00664881`, p `0.00990099`)
- GLM/Hermes base -> prompt_set_02 remains open at this ablation gate:
  endpoint-feature p `0.089108911`, edge-key p `0.554455446`
- Gemma base -> rerun_02 supports endpoint-feature ablation
  (`drop=0.027043001`, p `0.03960396`), while exact edge-key ablation remains
  just below support at p `0.069306931`
- Gemma base -> prompt_set_02 supports exact edge-key ablation
  (`drop=0.005148016`, p `0.01980198`), while endpoint-feature ablation remains
  open at p `0.237623762`
- clean read: direct SAE recurrent-branch ablation is partial but real. The
  recurrent feature/circuit paths can move transfer readout beyond matched
  random removals, with branch-specific differences between endpoint-feature
  removal and exact edge-key removal.

The current bridge is:

```text
hidden states -> attention flow -> MLP updates -> SAE feature/circuit tracing
```

## Next Execution Order

1. Run MLP depth recurrence after SAE recurrent-branch ablation is logged.
2. Move into `Nest 2D` allostery, then `Nest 2E` PFAS safety, `Nest 2F`
   materials, and `Nest 2G` descriptor/model controls.
