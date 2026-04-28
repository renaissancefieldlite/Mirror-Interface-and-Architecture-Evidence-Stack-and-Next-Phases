# GRAPH-2B Raw Token / Layer Pathway Report

Status: `completed_no_control_support_internal_graph2b`

GRAPH-2B ran on real raw token/layer point-cloud inputs but did not beat the locked controls.

## Inputs

- Point-cloud source: `artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- Label source: `artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_data_2026-04-22.json`
- Primary label mode: `phase6_amplitude_top3`
- Positive pairs: `GLM|Hermes, GLM|Mistral, Hermes|Mistral`

## Graph

- `node_count`: `16416`
- `edge_count`: `57555`
- `local_edge_count`: `29784`
- `cross_edge_count`: `27771`
- `model_count`: `8`
- `models`: `DeepSeek, GLM, Gemma, Hermes, Mistral, Nemotron, Qwen, SmolLM3`
- `scored_signature_rows`: `18144`
- `cluster_rows`: `28`

## Cluster Metrics

- `mirror_path_auc`: `0.413333`
- `degree_baseline_auc`: `0.52`
- `mirror_minus_degree_auc`: `-0.106667`
- `mirror_path_auc_exact_label_shuffle_p`: `0.68895`
- `degree_baseline_auc_exact_label_shuffle_p`: `0.472222`

## Row Metrics

- `mirror_path_auc`: `0.470933`
- `degree_baseline_auc`: `0.575592`
- `mirror_minus_degree_auc`: `-0.104659`
- `mirror_path_auc_pair_label_shuffle_p`: `0.614469`

## Perturbation Controls

### layer_order

- `row_mirror_path_auc`: `0.469265`
- `row_degree_baseline_auc`: `0.575875`
- `row_pair_label_shuffle_p`: `0.618132`
- `cluster_mirror_path_auc`: `0.373333`
- `cluster_degree_baseline_auc`: `0.52`
- `cluster_exact_label_shuffle_p`: `0.761294`

### token_window

- `row_mirror_path_auc`: `0.47344`
- `row_degree_baseline_auc`: `0.575634`
- `row_pair_label_shuffle_p`: `0.602869`
- `cluster_mirror_path_auc`: `0.426667`
- `cluster_degree_baseline_auc`: `0.52`
- `cluster_exact_label_shuffle_p`: `0.663309`

## Boundary

This is an internal raw token/layer graph validation over V8 point-cloud exports and Phase 6 quantum labels. It does not validate external molecular pathways, allostery, attention-flow, grid-flow, logistics, chemistry, or universal graph structure.

## Next Step

If cluster-level support remains open, the next GRAPH-2 fork should use a real independent domain graph: attention-flow if exported, then Nest 2 molecular/allostery labels, then grid/logistics flow labels when those datasets exist.
