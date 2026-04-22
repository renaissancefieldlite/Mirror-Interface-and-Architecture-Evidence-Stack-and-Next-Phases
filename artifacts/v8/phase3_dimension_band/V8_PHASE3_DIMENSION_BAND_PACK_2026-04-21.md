# V8 Phase 3 Dimension and Band Pack

Generated: `2026-04-21T18:13:38.145001+00:00`

## Summary

- most models show a razor-thin late band: a single-layer >=90% target peak band
- `Nemotron` and `SmolLM3` are the only multi-layer late-band rows in the current bridge
- `Mistral/Hermes` show a strong same-family peak-dimension overlap at the exact same layer
- same-hidden-size but different-family pairs do not show that same overlap pattern
- the Phase 3 outputs now form a clean handoff into the later `PennyLane/Qiskit` bridge

## Cross-Family Geometry Table

| Model | Hidden | Peak | Peak % | Band Layers | Band Width | last/target | Style | Variance Note |
| --- | ---: | ---: | ---: | --- | ---: | ---: | --- | --- |
| `Mistral` | `4096` | `31` | `96.88` | `31` | `1` | `0.579` | target-dominant compression | exact-match reruns after baseline |
| `Qwen` | `2048` | `34` | `94.44` | `34` | `1` | `0.708` | target-dominant compression | exact-match reruns after baseline |
| `Gemma` | `2560` | `41` | `97.62` | `41` | `1` | `1.443` | readout amplification | exact-match reruns after baseline |
| `DeepSeek` | `3584` | `26` | `92.86` | `26` | `1` | `0.635` | target-dominant compression | exact-match reruns after baseline |
| `Hermes` | `4096` | `31` | `96.88` | `31` | `1` | `0.666` | target-dominant compression | exact-match reruns after baseline |
| `GLM` | `4096` | `38` | `95.00` | `38` | `1` | `1.024` | balanced carry-through | exact-match reruns after baseline |
| `Nemotron` | `3136` | `40` | `95.24` | `39,40` | `2` | `1.271` | readout amplification | only live variance row |
| `SmolLM3` | `2048` | `34` | `94.44` | `34,35` | `2` | `0.556` | target-dominant compression | exact-match reruns after baseline |

## Same-Hidden-Size Overlap

| Pair | Hidden Size | Peak Layers | Overlap Count | Jaccard | Shared Dims |
| --- | ---: | --- | ---: | ---: | --- |
| `Mistral vs Hermes` | `4096` | `31/31` | `6` | `0.600000` | `552,705,777,1375,3244,3855` |
| `Mistral vs GLM` | `4096` | `31/38` | `0` | `0.000000` | `` |
| `Qwen vs SmolLM3` | `2048` | `34/34` | `0` | `0.000000` | `` |
| `Hermes vs GLM` | `4096` | `31/38` | `0` | `0.000000` | `` |

## Quantum Bridge Handoff

Phase 3 now produces the structured feature candidates for the later quantum bridge:

- `peak_percentile`
- `band_width`
- `target_peak`
- `last_to_target_ratio`
- aggregate late-band top-dimension magnitudes
- same-hidden-size overlap score when valid

Use them later as:

- `PennyLane` for rapid encoding design and sweeps
- `Qiskit` for the formal simulator / observable mirror
- optional Bell-state testing only as calibration for the quantum-stack pipeline, not as the next required semantic proof rung

## Charts

- [v8_phase3_band_width_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase3_dimension_band_2026-04-21/charts/v8_phase3_band_width_2026-04-21.png)
- [v8_phase3_last_to_target_ratio_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase3_dimension_band_2026-04-21/charts/v8_phase3_last_to_target_ratio_2026-04-21.png)
- [v8_phase3_peak_percentile_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase3_dimension_band_2026-04-21/charts/v8_phase3_peak_percentile_2026-04-21.png)
- [v8_phase3_same_hidden_overlap_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase3_dimension_band_2026-04-21/charts/v8_phase3_same_hidden_overlap_2026-04-21.png)
