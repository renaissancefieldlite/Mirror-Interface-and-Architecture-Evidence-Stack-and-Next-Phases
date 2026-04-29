# V8 SAE Feature / Circuit Gate

Status: `source_inventory_complete_missing_sae_exports`

## Clean Read

Sparse Autoencoder features are the next interpretable proof layer after
hidden states, attention-flow, and MLP/feed-forward deltas.

The role is specific:

- hidden states show where the representation lands
- attention heads show token-routing flow
- MLP blocks show representation updates
- SAE features expose sparse interpretable feature activations and possible circuit paths

This gate is protocol-ready, not evidence-closed. No SAE feature/circuit
claim is promoted until real SAE activations, feature dictionaries, circuit
edges, and controls exist.

## Artifact State

- SAE model files: `0`
- feature activation files: `0`
- feature dictionary files: `0`
- circuit edge files: `0`
- ablation files: `0`
- source inventory report status: `bounded_training_inputs_ready`
- validation report status: `None`

## Required Exports

- `feature_activations`: `model`, `prompt_set`, `context`, `layer_index`, `layer_depth`, `token_index`, `token_role`, `feature_id`, `activation`, `sparsity`
- `feature_dictionary`: `model`, `layer_index`, `feature_id`, `top_tokens_or_terms`, `human_label_optional`, `decoder_norm`
- `feature_circuit_edges`: `model`, `prompt_set`, `context`, `source_layer`, `source_feature_id`, `target_layer`, `target_feature_id`, `edge_weight`, `edge_type`
- `optional_ablation`: `model`, `prompt_set`, `context`, `ablated_feature_or_edge`, `readout_delta`, `hidden_state_delta`

## Acceptance Rule

- `feature_layer`: lattice / mirror feature activations must separate from neutral / technical controls above shuffled context labels and feature-frequency baselines
- `circuit_layer`: feature-to-feature circuit paths must beat degree / centrality baselines and shuffled feature-label or shuffled-token-window controls
- `prompt_generalization`: supported SAE features or circuits must recur across base, rerun_02, and prompt_set_02 before claiming prompt-generalized feature/circuit structure
- `ablation`: optional stronger closeout: ablating top SAE features or circuit edges should move readout/hidden-state signatures more than matched control ablations

## Locked Missing Inputs

- bounded SAE pilot training on GLM and Hermes dense trajectory point-cloud activations
- SAE feature activation export for the same standard model/prompt/context matrix
- feature dictionary or top-token labels for each exported SAE feature
- feature-to-feature circuit edge export across layers
- shuffled-label, shuffled-feature, shuffled-token-window, and degree/centrality controls
- optional ablation pass for causal circuit support

## Next Execution Order

1. train bounded SAE pilot on GLM and Hermes dense trajectory point-cloud activations
2. export feature activations for base, rerun_02, and prompt_set_02 on the standard model set
3. build feature dictionaries and topic labels for Mirror Interface / LSPS, quantum consciousness geometry, circuit-state bridge, neutral controls, and technical controls
4. construct feature-circuit edges across token roles and layers
5. validate feature separation and circuit-flow against locked controls
6. only then promote SAE from protocol gate to evidence layer
