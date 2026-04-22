# V8 Phase 2 Variance Pack

Generated: `2026-04-21T17:34:45.080584+00:00`

## Summary

- completed full `5`-run matrix: `run_01` baseline plus `run_02` through `run_05`
- all `8/8` models held the same strongest target layer across all five runs
- `7/8` models were exact-match across reruns `run_02` through `run_05`: `Mistral, Qwen, Gemma, DeepSeek, Hermes, GLM, SmolLM3`
- `Nemotron` was the only live variance row, but it remained anchored to the same late-layer structural slot

## Summary Table

| Model | Target Layers | Target Mean | Target Std | Target CI95 | Last Mean | Last Std | Note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `Mistral` | `31` | `247.851224` | `0.126864` | `0.111201` | `143.594378` | `0.091195` | exact-match reruns after baseline |
| `Qwen` | `34` | `126.971666` | `0.344844` | `0.302269` | `89.638243` | `0.099854` | exact-match reruns after baseline |
| `Gemma` | `41` | `77.107269` | `0.112578` | `0.098679` | `113.200110` | `0.921184` | exact-match reruns after baseline |
| `DeepSeek` | `26` | `326.400085` | `3.159824` | `2.769708` | `217.337878` | `3.598904` | exact-match reruns after baseline |
| `Hermes` | `31` | `248.102890` | `0.116178` | `0.101834` | `165.302338` | `0.033198` | exact-match reruns after baseline |
| `GLM` | `38` | `479.279107` | `0.009676` | `0.008482` | `487.051514` | `2.023775` | exact-match reruns after baseline |
| `Nemotron` | `40` | `207.306494` | `5.907646` | `5.178280` | `286.170248` | `29.904844` | only live variance row |
| `SmolLM3` | `34` | `20.830145` | `0.000000` | `0.000000` | `11.582764` | `0.000000` | exact-match reruns after baseline |

## Charts

- [v8_phase2_target_delta_by_run_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_residual_stream_variance_2026-04-21/phase2_variance_pack/charts/v8_phase2_target_delta_by_run_2026-04-21.png)
- [v8_phase2_target_mean_errorbars_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_residual_stream_variance_2026-04-21/phase2_variance_pack/charts/v8_phase2_target_mean_errorbars_2026-04-21.png)
- [v8_phase2_peak_layer_stability_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_residual_stream_variance_2026-04-21/phase2_variance_pack/charts/v8_phase2_peak_layer_stability_2026-04-21.png)
- [v8_phase2_flagship_boundary_profiles_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_residual_stream_variance_2026-04-21/phase2_variance_pack/charts/v8_phase2_flagship_boundary_profiles_2026-04-21.png)
