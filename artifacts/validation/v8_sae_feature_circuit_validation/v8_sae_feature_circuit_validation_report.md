# V8 SAE Bounded Pilot Report

Status: `feature_separation_supported_circuit_edges_exported`

## Clean Read

Bounded SAE pilot trained on real GLM / Hermes dense V8 activations. Sparse features separate lattice / neutral / technical contexts above shuffled-label controls, and feature-to-feature edge exports are ready for the next circuit / ablation gate.

## Inputs

- dense rows sampled: `10566`
- hidden size: `4096`
- latent features: `64`
- max rows per model/context/layer-depth/token-region group: `180`

## Training

- final reconstruction MSE: `0.604151`
- final sparse activation L1: `0.502900`
- mean feature sparsity: `0.614923`

## Feature-Control Validation

- observed balanced accuracy: `0.632462`
- shuffled balanced accuracy mean: `0.330598`
- shuffled balanced accuracy p95: `0.362288`
- shuffled-control p-value: `0.009901`
- feature separation supported: `True`

## Exports

- `model`: `artifacts/validation/v8_sae_feature_circuit_exports/sae_models/v8_sae_bounded_pilot_state.pt`
- `feature_activations`: `artifacts/validation/v8_sae_feature_circuit_exports/v8_sae_feature_activations.csv`
- `feature_dictionary`: `artifacts/validation/v8_sae_feature_circuit_exports/v8_sae_feature_dictionary.csv`
- `feature_circuit_edges`: `artifacts/validation/v8_sae_feature_circuit_exports/v8_sae_feature_circuit_edges.csv`
- `edge_count`: `5000`

## Next Gates

- run feature/circuit edge controls beyond label-shuffle feature separation
- add prompt_set_02 and rerun_02 SAE exports for prompt-generalized feature support
- run optional ablations on top SAE features and top feature-circuit edges
