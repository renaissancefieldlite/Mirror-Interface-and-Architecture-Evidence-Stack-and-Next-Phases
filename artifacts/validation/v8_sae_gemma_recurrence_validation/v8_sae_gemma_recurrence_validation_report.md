# V8 SAE Gemma Recurrence Validation Report

Status: `sae_gemma_recurrence_supported`

## Clean Read

Gemma is now integrated as a model-native SAE branch. The Gemma SAE recurrence run trains on real Gemma base dense V8 activations and carries the locked Gemma encoder into rerun_02 and prompt_set_02, giving the next gates a third-model SAE recurrence surface alongside GLM / Hermes.

## Why Gemma Gets A Native Branch

Gemma dense V8 vectors are 2560-dimensional, while the first GLM / Hermes SAE branch is 4096-dimensional. This run keeps the evidence clean by training a Gemma-native SAE on Gemma base vectors, then applying that same locked Gemma encoder to rerun_02 and prompt_set_02.

## Sample

### base

- rows: `5355`
- features: `64`
- context counts: `{'lattice': 1785, 'neutral': 1785, 'technical': 1785}`

### rerun_02

- rows: `5355`
- features: `64`
- context counts: `{'lattice': 1785, 'neutral': 1785, 'technical': 1785}`

### prompt_set_02

- rows: `5355`
- features: `64`
- context counts: `{'lattice': 1785, 'neutral': 1785, 'technical': 1785}`

## Within-Set Feature Separation

- `base`: balanced accuracy `0.479140512`, shuffle p95 `0.361626912`, p `0.00990099`, supported `True`
- `rerun_02`: balanced accuracy `0.493431208`, shuffle p95 `0.369158297`, p `0.00990099`, supported `True`
- `prompt_set_02`: balanced accuracy `0.418165016`, shuffle p95 `0.354145162`, p `0.00990099`, supported `True`

## Base-To-Set Transfer

- `base_to_rerun_02`: balanced accuracy `0.510737628`, shuffle p95 `0.354827264`, p `0.00990099`, supported `True`
- `base_to_prompt_set_02`: balanced accuracy `0.389542484`, shuffle p95 `0.351774043`, p `0.00990099`, supported `True`

## Feature Lift Recurrence

- `base_to_rerun_02`: cosine `0.967395663`, top-feature jaccard `0.538461538`, shared top features `[3, 9, 15, 23, 25, 38, 49]`
- `base_to_prompt_set_02`: cosine `0.392933488`, top-feature jaccard `0.176470588`, shared top features `[3, 49, 50]`

## Training History

- epoch `1`: loss `1.014238`, mse `1.014025`, l1 `0.212264`
- epoch `2`: loss `0.938377`, mse `0.938101`, l1 `0.276397`
- epoch `3`: loss `0.869490`, mse `0.869128`, l1 `0.361604`
- epoch `4`: loss `0.823180`, mse `0.822752`, l1 `0.428212`
- epoch `5`: loss `0.790688`, mse `0.790210`, l1 `0.478238`
- epoch `6`: loss `0.763860`, mse `0.763342`, l1 `0.517980`
- epoch `7`: loss `0.742647`, mse `0.742095`, l1 `0.552571`
- epoch `8`: loss `0.724385`, mse `0.723800`, l1 `0.585437`

## Exports

- `feature_profiles`: `artifacts/validation/v8_sae_gemma_recurrence_validation/v8_sae_gemma_recurrence_feature_profiles.csv`
- `sae_state`: `artifacts/validation/v8_sae_gemma_recurrence_validation/sae_models/v8_sae_gemma_recurrence_state.pt`

## Next Gates

- run SAE feature-edge recurrence with GLM / Hermes plus the Gemma-native branch
- run direct SAE feature/circuit ablations across recurrent branches
- run MLP depth recurrence after SAE recurrence is logged
- move to Nest 2D allostery, 2E PFAS safety, 2F materials, and 2G descriptor/model controls
