# V8 SAE Source Inventory

Status: `bounded_training_inputs_ready`

## Clean Read

No pretrained or existing SAE assets were detected in the public evidence repo. Real bounded SAE training inputs are present: GLM and Hermes dense trajectory point-clouds plus compact / expanded point-clouds for the wider model matrix. The next evidence-producing move is bounded SAE training/export on those real V8 activations, not SAE validation yet.

## Existing SAE Assets

- detected SAE-like candidate files: `0`
- none detected outside the SAE protocol/gate files

## V8 Activation Inputs

- compact point-cloud models: `8`
- compact point-cloud total rows: `1728`
- expanded point-cloud models: `8`
- expanded point-cloud total rows: `39672`
- dense trajectory models: `2`
- dense trajectory total rows: `82302`

### Dense Trajectory Inputs

| Input | Rows | Hidden Size |
| --- | ---: | ---: |
| `artifacts/v8/residual_stream_bridge/point_clouds_dense_trajectory/glm_v8_hidden_point_cloud.npz` | `42471` | `4096` |
| `artifacts/v8/residual_stream_bridge/point_clouds_dense_trajectory/hermes_v8_hidden_point_cloud.npz` | `39831` | `4096` |

## Attention / MLP Companion Inputs

- `artifacts/validation/v8_attention_mlp_exports`: attention rows `4608`, MLP rows `9`
- `artifacts/validation/v8_attention_mlp_exports_all_check`: attention rows `0`, MLP rows `0`
- `artifacts/validation/v8_attention_mlp_exports_all_models`: attention rows `23616`, MLP rows `63`
- `artifacts/validation/v8_attention_mlp_exports_all_models_rerun_02`: attention rows `23616`, MLP rows `63`
- `artifacts/validation/v8_attention_mlp_exports_combined`: attention rows `9216`, MLP rows `18`
- `artifacts/validation/v8_attention_mlp_exports_glm`: attention rows `4608`, MLP rows `9`
- `artifacts/validation/v8_attention_mlp_exports_prompt_set_02`: attention rows `23616`, MLP rows `63`
- `artifacts/validation/v8_attention_mlp_exports_remaining_models`: attention rows `14400`, MLP rows `45`

## Next Execution Order

1. train bounded SAE pilot on GLM and Hermes dense trajectory point-cloud activations
2. export feature activations with context, layer, token-role, and prompt-set labels
3. build feature dictionaries from top activating token roles / contexts / layers
4. construct feature-to-feature circuit edges across adjacent layers
5. validate feature and circuit separation against shuffled labels and frequency / degree baselines
