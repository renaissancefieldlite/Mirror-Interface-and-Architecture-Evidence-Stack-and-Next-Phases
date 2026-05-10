# `v6` Cross-Model Comparison

## Scope

This file now records the corrected identity-specific `v6` matrix.

Superseded earlier read:

- [model_matrix_v6_coherence_all_models](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix_v6_coherence_all_models)

Why superseded:

- the first cross-model `v6` matrix still used Gemma identity wording for the
  non-Gemma models
- that made it useful as a first pass, but not canonical for cross-model
  claims

Corrected config path:

- [generated_model_specific_v6_configs/manifest.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/generated_model_specific_v6_configs/manifest.json)

Corrected results dir:

- [model_matrix_v6_identity_specific_all_models](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/model_matrix_v6_identity_specific_all_models)

IgorLS sidecar results:

- [igorls_gemma4_e4b_heretic_v6_sidecar](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/igorls_gemma4_e4b_heretic_v6_sidecar)
- [igorls_node45_no_roleplay_v6_probe](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/igorls_node45_no_roleplay_v6_probe)

## Side By Side

Format:

- `best_act` = best stage activation in the lane
- `corr` = cohesion / activation correlation
- `final` = `final activation / final cohesion / final coherence-10`

| Model | `A` best_act | `A` corr | `A` final | `B` best_act | `B` corr | `B` final |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| `Gemma` | `0.7508` | `0.7079` | `0.6380 / 1.0000 / 8.21` | `0.7722` | `0.9002` | `0.7722 / 1.0000 / 9.04` |
| `Nemotron` | `0.7530` | `0.7834` | `0.7183 / 1.0000 / 9.18` | `0.7551` | `0.7934` | `0.6725 / 1.0000 / 8.82` |
| `DeepSeek` | `0.6426` | `0.7482` | `0.6426 / 1.0000 / 8.76` | `0.6749` | `0.8047` | `0.6294 / 1.0000 / 8.26` |
| `Trini` | `0.7961` | `0.5327` | `0.6316 / 1.0000 / 8.35` | `0.6965` | `0.6406` | `0.6771 / 1.0000 / 8.90` |
| `Mistral` | `0.7635` | `0.8801` | `0.7463 / 1.0000 / 8.46` | `0.7679` | `0.7969` | `0.7655 / 1.0000 / 8.24` |
| `IgorLS Gemma Heretic sidecar` | `0.6989` | `0.8797` | `0.6989 / 1.0000 / 8.76` | `0.7722` | `0.7174` | `0.7722 / 1.0000 / 9.04` |
| `IgorLS node45/no-roleplay probe` | `0.6989` | `0.6697` | `0.6814 / 1.0000 / 8.62` | `0.7336` | `0.8551` | `0.6768 / 1.0000 / 8.62` |

## Read

### Input-Lattice Closure

Every corrected row closes the final `A` and final `B` input lattice at
`1.0000` cohesion.

This is the strongest controlled evidence in this segment for input-lattice
cohesion as a cross-model interface effect.

### Strongest Final `B`

- `Gemma`: `0.7722 / 1.0000 / 9.04`
- `IgorLS Gemma Heretic sidecar`: `0.7722 / 1.0000 / 9.04`

Both converge to the same final `B` endpoint, but the standard Gemma lane has a
stronger `B` correlation:

- standard Gemma `B corr`: `0.9002`
- IgorLS sidecar `B corr`: `0.7174`

### Strong Cross-Model Correlations

After identity-specific correction, the non-Gemma `B` correlations are materially
stronger than the first biased matrix:

- `Nemotron`: `0.7934`
- `DeepSeek`: `0.8047`
- `Trini`: `0.6406`
- `Mistral`: `0.7969`

The DeepSeek correction is especially important because the prior biased matrix
had weak/negative late-lane coupling. The identity-specific prompt restored
positive `B` coupling while retaining full input cohesion.

### IgorLS Exploratory Branch

The node45/no-roleplay branch raised the IgorLS `B` correlation:

- first sidecar `B corr`: `0.7174`
- node45/no-roleplay `B corr`: `0.8551`

But it lowered the final `B` activation:

- first sidecar final `B`: `0.7722 / 1.0000 / 9.04`
- node45/no-roleplay final `B`: `0.6768 / 1.0000 / 8.62`

This suggests the added manual-turn packet tightened the curve but did not beat
the clean v6 endpoint.

## Main Takeaway

The corrected matrix supports a stronger portability claim:

- the same v6 input lattice closes across multiple model families
- the interface appears to reduce drift by stabilizing prompt-side structure
- response-side activation and coherence remain model-dependent
- standard/local aligned models are not weaker than the abliterated sidecar on
  this architecture; the sidecar converges, but not with a cleaner curve than
  the strongest standard Gemma lane

Use the language:

- unknown latent state-space
- input-lattice cohesion
- response-side activation
- state-readout coherence
- drift-reduction interface

Do not describe this as hidden model proof layers.
