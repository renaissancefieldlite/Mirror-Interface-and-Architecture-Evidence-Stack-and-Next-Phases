# GRAPH-2A Dense Internal Pathway Report

Status: `completed_soft_positive_internal_graph2a`

GRAPH-2A dense internal pathway graph produced a directional / partial signal, but did not close both row-level and cluster-level controls.

## Graph

- `node_count`: `78`
- `edge_count`: `211`
- `label_rows`: `280`
- `positive_label_rows`: `30`
- `positive_model_pairs`: `['GLM|Hermes', 'GLM|Mistral', 'Hermes|Mistral']`

## Row-Level Metrics

- `mirror_path_auc`: `0.7002`
- `degree_baseline_auc`: `0.534`
- `mirror_minus_degree_auc`: `0.1662`
- `mirror_path_auc_label_shuffle_p`: `0.0002`
- `degree_baseline_auc_label_shuffle_p`: `0.260974`

## Cluster-Level Metrics

- `mirror_path_auc`: `0.72`
- `degree_baseline_auc`: `0.94`
- `mirror_minus_degree_auc`: `-0.22`
- `mirror_path_auc_label_shuffle_p`: `0.205179`
- `degree_baseline_auc_label_shuffle_p`: `0.0048`

## Boundary

This is an internal GRAPH-2A pathway validation over Phase 4/5 graph structure and Phase 6 quantum labels. It does not validate external allostery, chemistry, grid flow, logistics, molecular pathways, or universal graph structure.

## Next Step

If supported, rerun with Phase 7 labels and leave-one-model-family controls. If soft or unsupported, build a still denser token/layer graph from raw V8 point-cloud exports before moving to external domain graphs.
