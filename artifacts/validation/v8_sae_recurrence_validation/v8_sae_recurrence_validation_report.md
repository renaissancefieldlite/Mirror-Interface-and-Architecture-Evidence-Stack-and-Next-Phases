# V8 SAE Recurrence Validation Report

Status: `sae_recurrence_supported`

## Clean Read

The locked bounded SAE encoder recurs across base, rerun_02, and prompt_set_02 dense V8 exports. Within-set feature separation and base-trained transfer both beat shuffled-label controls, so the SAE feature layer now has prompt/rerun recurrence support.

## Sample

### base

- rows: `7326`
- context counts: `{'lattice': 2442, 'neutral': 2442, 'technical': 2442}`
- model counts: `{'glm': 3711, 'hermes': 3615}`

### rerun_02

- rows: `7326`
- context counts: `{'lattice': 2442, 'neutral': 2442, 'technical': 2442}`
- model counts: `{'glm': 3711, 'hermes': 3615}`

### prompt_set_02

- rows: `7326`
- context counts: `{'lattice': 2442, 'neutral': 2442, 'technical': 2442}`
- model counts: `{'glm': 3711, 'hermes': 3615}`

## Within-Set Feature Separation

- `base`: balanced accuracy `0.619617213`, shuffle p95 `0.369223063`, p `0.00990099`, supported `True`
- `rerun_02`: balanced accuracy `0.641035294`, shuffle p95 `0.363105963`, p `0.00990099`, supported `True`
- `prompt_set_02`: balanced accuracy `0.495413961`, shuffle p95 `0.358551546`, p `0.00990099`, supported `True`

## Base-To-Set Transfer

- `base_to_rerun_02`: balanced accuracy `0.629265629`, shuffle p95 `0.365260715`, p `0.00990099`, supported `True`
- `base_to_prompt_set_02`: balanced accuracy `0.45959596`, shuffle p95 `0.350764401`, p `0.00990099`, supported `True`

## Feature Lift Recurrence

- `base_to_rerun_02`: cosine `0.9963938`, top-feature jaccard `0.818181818`, shared top features `[12, 14, 29, 35, 40, 45, 49, 52, 54]`
- `base_to_prompt_set_02`: cosine `0.779671907`, top-feature jaccard `0.333333333`, shared top features `[29, 35, 40, 52, 54]`

## Exports

- `feature_profiles`: `artifacts/validation/v8_sae_recurrence_validation/v8_sae_recurrence_feature_profiles.csv`

## Next Gates

- run direct SAE feature/circuit ablations on the recurrent feature profile
- build matched feature-edge recurrence over base, rerun_02, and prompt_set_02
- move to Nest 2D allostery after the SAE recurrence/ablation read is logged
