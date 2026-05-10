# V8 SAE Recurrent Branch Ablation V2 Report

Status: `sae_recurrent_branch_ablation_v2_supported`

## Clean Read

The targeted SAE recurrent-branch ablation v2 closes the GLM/Hermes prompt_set_02 weak case under stronger shared-path capture and 500-trial controls.

## Target

- branch: `glm_hermes`
- transfer: `base -> prompt_set_02`
- full transfer balanced accuracy: `0.396043387`

## Best Confirmed Candidates

### weighted_recurrent_k1000_endpoint_feature

- removal: `endpoint_feature`
- top_k: `1000`
- edge keys: `1000`
- features removed: `38`
- ablation drop: `0.396043387`
- random p95 / p99: `0.050921468` / `0.061189767`
- p-value: `0.005988024`
- supported: `True`
- rows after ablation: train `29`, test `36`

### weighted_recurrent_k1000_edge_key

- removal: `edge_key`
- top_k: `1000`
- edge keys: `1000`
- features removed: `38`
- ablation drop: `0.027632329`
- random p95 / p99: `-0.0041044` / `-0.002357068`
- p-value: `0.001996008`
- supported: `True`
- rows after ablation: train `4000`, test `4000`

### weighted_recurrent_k500_edge_key

- removal: `edge_key`
- top_k: `500`
- edge keys: `500`
- features removed: `33`
- ablation drop: `0.025587609`
- random p95 / p99: `-0.001268942` / `0.000111553`
- p-value: `0.001996008`
- supported: `True`
- rows after ablation: train `4500`, test `4500`

### weighted_recurrent_k250_endpoint_feature

- removal: `endpoint_feature`
- top_k: `250`
- edge keys: `250`
- features removed: `27`
- ablation drop: `0.058192729`
- random p95 / p99: `0.040745989` / `0.046481952`
- p-value: `0.001996008`
- supported: `True`
- rows after ablation: train `3084`, test `3159`

### top_overlap_k1000_edge_key

- removal: `edge_key`
- top_k: `1000`
- edge keys: `344`
- features removed: `29`
- ablation drop: `0.014680568`
- random p95 / p99: `-0.000111803` / `0.001111848`
- p-value: `0.001996008`
- supported: `True`
- rows after ablation: train `4656`, test `4656`

### top_overlap_k1000_endpoint_feature

- removal: `endpoint_feature`
- top_k: `1000`
- edge keys: `344`
- features removed: `29`
- ablation drop: `0.058914327`
- random p95 / p99: `0.044600379` / `0.050418767`
- p-value: `0.001996008`
- supported: `True`
- rows after ablation: train `2994`, test `3076`

## Interpretation Note

The broad endpoint-feature removals identify high-impact recurrent SAE features.
The sharper circuit-path read is the exact edge-key result, because those
ablations leave thousands of rows in train/test while still beating matched
random removals.

## Screen Summary

- screened candidates: `18`
- screen random trials: `100`
- confirm random trials: `500`
- confirmed candidates: `6`

## Next Gates

- update SAE protocol with v2 support
- run MLP depth recurrence before Nest 2D allostery
