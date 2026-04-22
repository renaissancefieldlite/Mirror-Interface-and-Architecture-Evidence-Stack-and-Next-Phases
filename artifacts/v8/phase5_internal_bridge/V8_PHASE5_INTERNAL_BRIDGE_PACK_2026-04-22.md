# V8 Phase 5 Internal Bridge Pack

Generated: `2026-04-22T08:35:30.024360+00:00`

## Summary

- Phase 5 turns the locked Phase 4 localization pass into a bridge map of token-position sensitivity, phrase localization, and context-to-readout behavior.
- No model is purely target-focused in the current bridge; the packet sharpens through family-specific context and readout paths instead.
- front-context rows: `Qwen, DeepSeek, Nemotron`
- late-context rows: `Mistral, Hermes, GLM, SmolLM3`
- bridge rows: `GLM, Nemotron`
- readout-led row: `Gemma`
- Phase 4 variance stays visible here: `Mistral, Hermes, Gemma, GLM, DeepSeek` are exact localization reruns after baseline, while `Nemotron` remains anchor-stable but magnitude-drifting.

## Token-Position Sensitivity Table

| Model | Dominant Anchor | Anchor Layer | Layer Span | Context Peak | Target | Last | Target/Ctx | Last/Target | Path | Variance Note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `Mistral` | `mid` | `31` | `0` | `303.582184` | `247.907959` | `143.635162` | `0.817` | `0.579` | late-context supported target | exact-match reruns after baseline |
| `Qwen` | `early` | `34` | `0` | `165.875290` | `127.125885` | `89.682899` | `0.766` | `0.705` | front-context loaded | not in focused localization variance subset |
| `Gemma` | `last` | `41` | `0` | `86.914543` | `77.056923` | `113.612076` | `0.887` | `1.474` | readout-led | exact-match reruns after baseline |
| `DeepSeek` | `early` | `25` | `1` | `602.411987` | `324.986969` | `218.947357` | `0.539` | `0.674` | front-context loaded | exact-match reruns after baseline |
| `Hermes` | `mid` | `31` | `0` | `303.928741` | `248.050934` | `165.287491` | `0.816` | `0.666` | late-context supported target | exact-match reruns after baseline |
| `GLM` | `mid` | `38` | `0` | `601.968079` | `479.274780` | `486.146454` | `0.796` | `1.014` | late-context to readout bridge | exact-match reruns after baseline |
| `Nemotron` | `early` | `39` | `1` | `944.597412` | `202.348648` | `343.705292` | `0.214` | `1.699` | front-context to readout bridge | anchor stable, magnitude drifting |
| `SmolLM3` | `mid` | `35` | `1` | `24.294479` | `20.830145` | `11.582764` | `0.857` | `0.556` | late-context supported target | not in focused localization variance subset |

## Phrase Localization / Bridge Table

| Model | Target/Surround | Target Layer | Last Layer | Dominant↔Target Overlap | Jaccard | Top-3 Anchor Sequence | Shared Dims |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `Mistral` | `0.914` | `31` | `31` | `3` | `0.231` | `mid > pre > target` | `835,1375,3855` |
| `Qwen` | `0.784` | `34` | `34` | `0` | `0.000` | `early > pre > mid` | `none` |
| `Gemma` | `1.005` | `41` | `41` | `0` | `0.000` | `last > mid > target` | `none` |
| `DeepSeek` | `0.704` | `26` | `26` | `1` | `0.067` | `early > pre > mid` | `2570` |
| `Hermes` | `0.884` | `31` | `31` | `4` | `0.333` | `mid > pre > target` | `1375,1641,3244,3855` |
| `GLM` | `0.853` | `38` | `38` | `2` | `0.143` | `mid > pre > early` | `2724,3665` |
| `Nemotron` | `0.754` | `40` | `39` | `0` | `0.000` | `early > mid > last` | `none` |
| `SmolLM3` | `0.869` | `34` | `34` | `0` | `0.000` | `mid > early > pre` | `none` |

## Main Read

- `Mistral` and `Hermes` remain the clearest late-context same-family bridge pair: `mid` dominates, `target` stays strong, and their dominant/target dim overlap is the cleanest in the set.
- `Qwen` and `DeepSeek` keep the front-context signature, with `DeepSeek` carrying much larger magnitude while still staying target-supportive rather than purely readout-led.
- `Gemma` remains the clearest readout-led row: `last` dominates and target/support windows sit below the readout surface.
- `GLM` and `Nemotron` are the bridge rows for different reasons: `GLM` carries strong late-context into readout almost one-to-one, while `Nemotron` swings from huge early-context loading into strong readout gain.
- `SmolLM3` stays the useful diffuse boundary row: still context-loaded, but smaller and more weakly coupled to readout than the flagship rows.

## PennyLane / Qiskit Handoff

Phase 5 sharpens the later quantum-bridge feature set beyond Phase 3 alone. The clean candidate features now are:

- `dominant_anchor_class`
- `target_to_context`
- `target_to_surround`
- `last_to_target`
- `anchor_layer_span`
- `dominant_target_dim_overlap_count`
- `dominant_target_dim_overlap_jaccard`

Use them later as:

- `PennyLane` for rapid encoding design and sweeps
- `Qiskit` for the formal simulator / observable mirror
- Bell-state testing only as later calibration for the quantum-stack pipeline, not as the current proof rung

## Charts

- [v8_phase5_anchor_heatmap_2026-04-22.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase5_internal_bridge_2026-04-22/charts/v8_phase5_anchor_heatmap_2026-04-22.png)
- [v8_phase5_bridge_scatter_2026-04-22.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase5_internal_bridge_2026-04-22/charts/v8_phase5_bridge_scatter_2026-04-22.png)
- [v8_phase5_dim_overlap_2026-04-22.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase5_internal_bridge_2026-04-22/charts/v8_phase5_dim_overlap_2026-04-22.png)
- [v8_phase5_anchor_layer_span_2026-04-22.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase5_internal_bridge_2026-04-22/charts/v8_phase5_anchor_layer_span_2026-04-22.png)
