# V8 Phase 4 Localization Variance Pack

Generated: `2026-04-22T03:31:25.895167+00:00`

## Summary

- available runs: `run_01, run_02, run_03, run_04, run_05`
- this pack tracks whether dominant anchor, target-span separation, and readout path remain stable across the focused localization subset
- exact-match reruns after baseline: `Mistral, Hermes, Gemma, GLM, DeepSeek`

## Summary Table

| Model | Dominant anchors | Target layers | Target mean | Target std | Last mean | Ratio mean | Note |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `Mistral` | `mid` | `31` | `247.907959` | `0.000000` | `143.635162` | `1.726` | exact-match reruns after baseline |
| `Hermes` | `mid` | `31` | `248.050934` | `0.000000` | `165.287491` | `1.501` | exact-match reruns after baseline |
| `Gemma` | `last_tok` | `41` | `77.056923` | `0.000000` | `113.612076` | `0.678` | exact-match reruns after baseline |
| `GLM` | `mid` | `38` | `479.274780` | `0.000000` | `486.146454` | `0.986` | exact-match reruns after baseline |
| `Nemotron` | `early` | `40` | `206.275735` | `5.012386` | `298.572632` | `0.696` | anchor stable, magnitude drifting |
| `DeepSeek` | `early` | `26` | `324.986969` | `0.000000` | `218.947357` | `1.484` | exact-match reruns after baseline |

## Charts

- [v8_phase4_localization_target_by_run_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase4_localization_variance_2026-04-21/phase4_localization_variance_pack/charts/v8_phase4_localization_target_by_run_2026-04-21.png)
- [v8_phase4_localization_last_by_run_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase4_localization_variance_2026-04-21/phase4_localization_variance_pack/charts/v8_phase4_localization_last_by_run_2026-04-21.png)
- [v8_phase4_localization_ratio_mean_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase4_localization_variance_2026-04-21/phase4_localization_variance_pack/charts/v8_phase4_localization_ratio_mean_2026-04-21.png)
- [v8_phase4_localization_anchor_layer_by_run_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase4_localization_variance_2026-04-21/phase4_localization_variance_pack/charts/v8_phase4_localization_anchor_layer_by_run_2026-04-21.png)
