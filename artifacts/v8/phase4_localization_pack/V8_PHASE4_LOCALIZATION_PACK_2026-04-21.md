# V8 Phase 4 Localization Pack

Generated: `2026-04-21T19:20:31.151342+00:00`

## Summary

- Phase 4 is the next internal bridge rung after the integrated V7+V8 pack
- it asks where the separation sharpens: early context, pre-target, target phrase, post-target, or last-token readout
- the first full localization matrix is now complete across the current 8-model bridge

## Localization Table

| Model | Dominant Anchor | Anchor Layer | Anchor Delta | Target | Last Token | Target/Last | Style |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `Mistral` | `mid` | `31` | `303.582184` | `247.907959` | `143.635162` | `1.726` | context-loaded |
| `Qwen` | `early` | `34` | `165.875290` | `127.125885` | `89.682899` | `1.418` | context-loaded |
| `Gemma` | `last_tok` | `41` | `113.612076` | `77.056923` | `113.612076` | `0.678` | readout-amplified |
| `DeepSeek` | `early` | `25` | `602.411987` | `324.986969` | `218.947357` | `1.484` | context-loaded |
| `Hermes` | `mid` | `31` | `303.928741` | `248.050934` | `165.287491` | `1.501` | context-loaded |
| `GLM` | `mid` | `38` | `601.968079` | `479.274780` | `486.146454` | `0.986` | context-loaded / readout-sensitive |
| `Nemotron` | `early` | `39` | `944.597412` | `202.348648` | `343.705292` | `0.589` | context-loaded / readout-sensitive |
| `SmolLM3` | `mid` | `35` | `24.294479` | `20.830145` | `11.582764` | `1.798` | context-loaded |

## Main Read

- `Mistral` and `Hermes` form the cleanest same-family localization pair: strong late-path structure with target phrase support but even stronger surrounding late packet structure.
- `Gemma` is the clearest readout-amplification localization row: `last_token` dominates over `target_span`.
- `Nemotron` is strongly context-loaded and readout-sensitive, with a huge `early_window` anchor and a still-strong last-token read.
- `GLM` is the strongest globally loaded localization row so far, combining broad packet loading with very strong readout carry-through.
- `Qwen` and `DeepSeek` form a context-loaded family pair, with `DeepSeek` carrying much larger magnitude.
- `SmolLM3` remains the diffuse boundary row.

## Style Buckets

- context-loaded models: `Mistral, Qwen, DeepSeek, Hermes, GLM, Nemotron, SmolLM3`
- readout-amplified models: `Gemma`
- target-localized models: `none in this first matrix`

## Why This Matters

Phase 4 shows that the internal separation is not uniformly distributed across token positions. Different families concentrate the effect differently: some in surrounding late context, some in readout, and some as hybrid context-to-readout paths.

That means the next bridge is no longer only 'where is the peak layer?' but also 'how does the packet travel through the token path before readout?'

## Next Steps

- fold Phase 4 back into the integrated technical pack
- use the strongest localization features as inputs to the later `PennyLane / Qiskit` bridge
- if needed, run localization variance on a focused subset instead of the whole matrix

## Charts

- [v8_phase4_anchor_profiles_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase4_localization_probe_2026-04-21/phase4_localization_pack/charts/v8_phase4_anchor_profiles_2026-04-21.png)
- [v8_phase4_target_vs_last_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase4_localization_probe_2026-04-21/phase4_localization_pack/charts/v8_phase4_target_vs_last_2026-04-21.png)
- [v8_phase4_dominant_anchor_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase4_localization_probe_2026-04-21/phase4_localization_pack/charts/v8_phase4_dominant_anchor_2026-04-21.png)
- [v8_phase4_target_last_ratio_2026-04-21.png](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v8_phase4_localization_probe_2026-04-21/phase4_localization_pack/charts/v8_phase4_target_last_ratio_2026-04-21.png)
