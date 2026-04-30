# V8 SAE Feature-Edge Recurrence Report

Status: `sae_feature_edge_recurrence_partial`

## Clean Read

SAE feature-edge recurrence is split in a useful way. The GLM/Hermes 4096-dim branch closes cleanly: within-set edge separation is supported for base, rerun_02, and prompt_set_02, and base-trained edge transfer is supported into both recurrence sets. The Gemma-native 2560-dim branch shows supported base-trained edge transfer into rerun_02 and prompt_set_02, plus strong weighted edge-signature recurrence, while within-set Gemma edge separation remains open. The next move is direct SAE feature/circuit ablation across the recurrent branches.

## Branch Inputs

### glm_hermes

- models: `['glm', 'hermes']`
- hidden size: `4096`
- set rows: `{'base': 7326, 'rerun_02': 7326, 'prompt_set_02': 7326}`
- set edge rows: `{'base': 5000, 'rerun_02': 5000, 'prompt_set_02': 5000}`

### gemma

- models: `['gemma']`
- hidden size: `2560`
- set rows: `{'base': 5355, 'rerun_02': 5355, 'prompt_set_02': 5355}`
- set edge rows: `{'base': 4428, 'rerun_02': 4428, 'prompt_set_02': 4428}`

## Within-Set Edge Separation

### glm_hermes

- `base`: full-edge balanced accuracy `0.455882927`, p `0.00990099`, supported `True`; degree baseline `0.319082968`, hub baseline `0.362540797`
- `rerun_02`: full-edge balanced accuracy `0.464051642`, p `0.00990099`, supported `True`; degree baseline `0.309297636`, hub baseline `0.350157263`
- `prompt_set_02`: full-edge balanced accuracy `0.376823065`, p `0.00990099`, supported `True`; degree baseline `0.317648707`, hub baseline `0.35098471`

### gemma

- `base`: full-edge balanced accuracy `0.298720843`, p `0.99009901`, supported `False`; degree baseline `0.325808879`, hub baseline `0.334838224`
- `rerun_02`: full-edge balanced accuracy `0.282167043`, p `1.0`, supported `False`; degree baseline `0.322046652`, hub baseline `0.346124906`
- `prompt_set_02`: full-edge balanced accuracy `0.270127916`, p `1.0`, supported `False`; degree baseline `0.319789315`, hub baseline `0.35364936`

## Base-To-Set Edge Transfer

### glm_hermes

- `base_to_rerun_02`: full-edge balanced accuracy `0.52387397`, p `0.00990099`, supported `True`; degree baseline `0.370917841`, hub baseline `0.361096063`
- `base_to_prompt_set_02`: full-edge balanced accuracy `0.395827668`, p `0.00990099`, supported `True`; degree baseline `0.347822177`, hub baseline `0.344280791`

### gemma

- `base_to_rerun_02`: full-edge balanced accuracy `0.438121048`, p `0.00990099`, supported `True`; degree baseline `0.375338753`, hub baseline `0.351626016`
- `base_to_prompt_set_02`: full-edge balanced accuracy `0.367434508`, p `0.00990099`, supported `True`; degree baseline `0.346657633`, hub baseline `0.327009937`

## Weighted Edge-Signature Recurrence

### glm_hermes

- `base_to_rerun_02`: cosine `0.768127447`, top-edge Jaccard `0.459854015`, shared top edges `63`
- `base_to_prompt_set_02`: cosine `0.391837556`, top-edge Jaccard `0.075268817`, shared top edges `14`

### gemma

- `base_to_rerun_02`: cosine `0.803169721`, top-edge Jaccard `0.639344262`, shared top edges `78`
- `base_to_prompt_set_02`: cosine `0.528171679`, top-edge Jaccard `0.242236025`, shared top edges `39`

## Exports

- `edge_rows`: `artifacts/validation/v8_sae_feature_edge_recurrence/v8_sae_feature_edge_recurrence_edges.csv`

## Next Gates

- run direct SAE feature/circuit ablations across the recurrent branches
- run MLP depth recurrence after the SAE feature-edge recurrence read is logged
- move to Nest 2D allostery, 2E PFAS safety, 2F materials, and 2G descriptor/model controls
