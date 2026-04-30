# V8 SAE Recurrence Gate

Status: `sae_recurrence_input_pending_prompt_rerun_dense_vectors`

## Clean Read

SAE recurrence can run once base, rerun_02, and prompt_set_02 dense hidden-vector point clouds exist for the same model/context structure. Base GLM/Hermes dense vectors exist; matching rerun_02 and prompt_set_02 dense vectors are the required next inputs.

## Input State

| Input | Exists | NPZ Count |
| --- | ---: | ---: |
| `base_dense` | `True` | `2` |
| `rerun_02_dense` | `False` | `0` |
| `prompt_set_02_dense` | `False` | `0` |

## Next Gates

- export rerun_02 dense trajectory point clouds for GLM / Hermes
- export prompt_set_02 dense trajectory point clouds for GLM / Hermes
- apply the bounded SAE encoder to those matched dense vectors
- compare feature recurrence across base, rerun_02, and prompt_set_02
