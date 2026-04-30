# V8 SAE Feature / Circuit Gate

Status: `feature_separation_supported_circuit_edges_exported`

## Clean Read

Sparse Autoencoder features are the next interpretable proof layer after
hidden states, attention-flow, and MLP/feed-forward deltas.

The role is specific:

- hidden states show where the representation lands
- attention heads show token-routing flow
- MLP blocks show representation updates
- SAE features expose sparse interpretable feature activations and possible circuit paths

Current support:

The bounded SAE pilot trained on real GLM / Hermes dense V8 activations, exported sparse feature activations, exported a feature dictionary, exported feature-to-feature circuit edges, and supported context separation above shuffled-label controls.

## Artifact State

- SAE model files: `1`
- feature activation files: `1`
- feature dictionary files: `1`
- circuit edge files: `1`
- ablation files: `0`
- source inventory report status: `bounded_training_inputs_ready`
- validation report status: `feature_separation_supported_circuit_edges_exported`

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

## Next Required Inputs

- edge-specific controls beyond the current shuffled-label feature separation
- prompt_set_02 and rerun_02 SAE exports for prompt-generalized feature support
- feature-frequency, degree, and centrality baselines for exported feature-circuit edges
- optional ablation pass for top SAE features and top feature-circuit edges

## Next Execution Order

1. run edge-specific controls on the exported feature-to-feature circuit graph
2. export SAE activations for rerun_02 and prompt_set_02
3. compare SAE feature recurrence across base, rerun_02, and prompt_set_02
4. run feature-frequency, degree, and centrality baselines
5. run optional ablations on top SAE features and top feature-circuit edges
