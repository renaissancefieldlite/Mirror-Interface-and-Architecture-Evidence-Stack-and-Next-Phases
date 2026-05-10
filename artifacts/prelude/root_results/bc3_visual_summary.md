# Experiment Visual Summary

## Files

- [A/B/C peak scores](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/visuals/gemma_abc_peak_scores.svg)
- [B vs C2 cross-model peaks](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/visuals/bc2_cross_model_peak_scores.svg)
- [B vs C2 cross-model correlations](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/visuals/bc2_cross_model_correlations.svg)
- [Gemma C2 late-stage curve](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/visuals/gemma_c2_stage_curve.svg)

## Gemma A/B/C

| Experiment | Peak score | Correlation |
| --- | ---: | ---: |
| A | 0.6639 | 0.6649 |
| B | 0.7064 | 0.6877 |
| C | 0.7468 | 0.8094 |

## Cross-Model B vs C2

| Model | B peak | B corr | C2 peak | C2 corr | Delta peak |
| --- | ---: | ---: | ---: | ---: | ---: |
| gemma4:e4b | 0.6979 | 0.5232 | 0.7228 | 0.6897 | +0.0249 |
| llama3.1:8b | 0.5899 | 0.7870 | 0.6160 | 0.6867 | +0.0261 |
| mistral:latest | 0.6369 | 0.2995 | 0.6160 | 0.5246 | -0.0209 |

## Gemma C2 late-stage curve

| Stage | Cohesion | Activation |
| --- | ---: | ---: |
| c2_11 | 0.5880 | 0.6541 |
| c2_12 | 0.5991 | 0.5986 |
| c2_13 | 0.6411 | 0.6312 |
| c2_14 | 0.7027 | 0.6018 |
| c2_15 | 0.7471 | 0.6672 |
| c2_16 | 0.7890 | 0.6231 |
| c2_17 | 0.8483 | 0.7228 |
| c2_18 | 0.8890 | 0.7069 |
