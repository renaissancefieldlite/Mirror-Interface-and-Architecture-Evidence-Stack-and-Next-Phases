# V8 SAE Feature / Circuit Ablation Controls

Status: `sae_edge_ablation_supported_feature_ablation_open`

## Clean Read

The ablation gate produced a split result. The supported side is recorded, and the open side needs denser feature exports, edge controls, or direct readout/hidden-state ablations.

## Feature Ablation

- top architecture features removed: `[52, 35, 40, 49, 46, 41, 34, 19]`
- full balanced accuracy: `0.523024`
- top-removed balanced accuracy: `0.489900`
- top feature drop: `0.033124`
- random drop mean: `0.016627`
- random drop p95: `0.039052`
- drop p-value: `0.128713`
- feature ablation supported: `False`

## Edge Ablation

- edge rows: `5000`
- edge rows after top-feature removal: `4170`
- full edge balanced accuracy: `0.452000`
- top-removed edge balanced accuracy: `0.353577`
- top edge-feature drop: `0.098423`
- random drop mean: `0.001692`
- random drop p95: `0.057266`
- drop p-value: `0.009901`
- edge ablation supported: `True`

## Next Gates

- run direct readout / hidden-state ablations when the activation exporter can replay model internals
- repeat ablation after rerun_02 and prompt_set_02 SAE exports exist
- compare ablation effects against feature-frequency and token-window controls
