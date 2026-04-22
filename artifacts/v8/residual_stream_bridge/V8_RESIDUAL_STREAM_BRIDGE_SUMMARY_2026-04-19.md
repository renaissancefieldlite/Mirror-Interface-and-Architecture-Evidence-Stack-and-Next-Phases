# V8 Residual-Stream Bridge Summary

Date: `2026-04-21T13:28:59.399661+00:00`

## Purpose

This summary reports internal hidden-state / residual-stream comparisons for the frozen V7 contextuality prompts.

## Run Status

- valid traced models: `8`
- missing / invalid models: `0`

## Layerwise Bridge Read

| Model | Comparison | Strongest target layer | Target delta | Target cosine | Strongest last layer | Last delta | Last cosine |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Mistral` | `lattice_vs_neutral` | `31` | `247.624283` | `0.667498` | `31` | `143.431244` | `0.938137` |
| `Mistral` | `lattice_vs_technical` | `31` | `223.346893` | `0.722084` | `31` | `156.763184` | `0.925089` |
| `Mistral` | `technical_vs_neutral` | `31` | `167.043869` | `0.845802` | `31` | `113.719055` | `0.961344` |
| `Qwen` | `lattice_vs_neutral` | `34` | `126.354790` | `0.939517` | `34` | `89.459618` | `0.955265` |
| `Qwen` | `lattice_vs_technical` | `34` | `127.071091` | `0.938318` | `34` | `96.162552` | `0.948137` |
| `Qwen` | `technical_vs_neutral` | `34` | `109.681923` | `0.954534` | `34` | `69.881310` | `0.970733` |
| `Gemma` | `lattice_vs_neutral` | `41` | `77.308655` | `0.629513` | `41` | `111.552246` | `0.784659` |
| `Gemma` | `lattice_vs_technical` | `41` | `75.144188` | `0.673466` | `41` | `106.351173` | `0.856226` |
| `Gemma` | `technical_vs_neutral` | `41` | `61.650166` | `0.729085` | `41` | `97.961586` | `0.880702` |
| `DeepSeek` | `lattice_vs_neutral` | `26` | `332.052551` | `0.948453` | `26` | `210.899963` | `0.983124` |
| `DeepSeek` | `lattice_vs_technical` | `26` | `316.486816` | `0.955633` | `26` | `241.915253` | `0.977918` |
| `DeepSeek` | `technical_vs_neutral` | `26` | `229.627243` | `0.976884` | `26` | `137.935287` | `0.992783` |
| `Hermes` | `lattice_vs_neutral` | `31` | `248.310715` | `0.650775` | `31` | `165.361725` | `0.905917` |
| `Hermes` | `lattice_vs_technical` | `31` | `232.648132` | `0.694990` | `31` | `174.763977` | `0.895176` |
| `Hermes` | `technical_vs_neutral` | `31` | `160.459427` | `0.850329` | `31` | `113.094170` | `0.957428` |
| `GLM` | `lattice_vs_neutral` | `38` | `479.296417` | `0.717402` | `38` | `490.671753` | `0.766960` |
| `GLM` | `lattice_vs_technical` | `38` | `453.863525` | `0.758231` | `38` | `868.385559` | `0.337363` |
| `GLM` | `technical_vs_neutral` | `38` | `375.284454` | `0.835651` | `38` | `662.077148` | `0.627867` |
| `Nemotron` | `lattice_vs_neutral` | `40` | `203.815063` | `0.878316` | `40` | `259.096069` | `0.848934` |
| `Nemotron` | `lattice_vs_technical` | `40` | `207.322479` | `0.877731` | `40` | `246.720871` | `0.860566` |
| `Nemotron` | `technical_vs_neutral` | `40` | `160.065628` | `0.927214` | `40` | `199.317719` | `0.914238` |
| `SmolLM3` | `lattice_vs_neutral` | `34` | `20.830145` | `0.656591` | `34` | `11.582764` | `0.930493` |
| `SmolLM3` | `lattice_vs_technical` | `34` | `17.987114` | `0.739326` | `34` | `10.503592` | `0.943511` |
| `SmolLM3` | `technical_vs_neutral` | `34` | `15.754481` | `0.800845` | `34` | `6.898580` | `0.976237` |

## Interpretation Boundary

V8 is the bridge from external behavioral SRM evidence into internal representational evidence. A valid V8 result requires local open-checkpoint traces; missing checkpoints are a setup state, not a negative result.
