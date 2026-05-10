# GRAPH-1/2 Pathway Validation Fork

Status: `completed_soft_positive_no_shuffle_support`

GRAPH-1/2 pathway validation completed; mirror path AUC beat degree baseline but did not beat shuffled-label controls.

## Requirements

- real graph edge CSV with source,target columns
- known pathway/control label CSV with source,target,label columns
- declared baseline such as degree centrality or random labels

## Metrics

- `node_count`: `8`
- `edge_count`: `16`
- `labeled_pair_count`: `28`
- `mirror_path_auc`: `0.74`
- `degree_baseline_auc`: `0.6467`
- `mirror_minus_degree_auc`: `0.0933`
- `mirror_path_auc_label_shuffle_p`: `0.166683`
- `mirror_path_auc_label_shuffle_mean`: `0.4986`
- `degree_baseline_auc_label_shuffle_p`: `0.237376`

## Boundary

This validates graph pathway recovery only; it does not validate chemistry, biology, or allostery without domain-correct labels.
