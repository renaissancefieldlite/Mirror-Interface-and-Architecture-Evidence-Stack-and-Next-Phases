# Nest 1 GRAPH Strengthened Pass

Status: `completed_local_strengthened_graph_pass`

The original GRAPH-lite binary kNN edge test was too blunt. The weighted/ranked Phase 6 feature-similarity graph gives a stronger expected-pair recovery signal, while Angle/Amplitude fidelity only strongly recover the Mistral/Hermes pair and do not close the full GRAPH lane by themselves.

## Input

- Phase 6 artifact: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_data_2026-04-22.json`
- Models: `Mistral, Qwen, Gemma, DeepSeek, Hermes, GLM, Nemotron, SmolLM3`
- Expected bridge pairs: `Hermes/Mistral, DeepSeek/Qwen, GLM/Nemotron`
- Control: `exact label permutation over real Phase 6 relation matrices`

## Weighted / Ranked Views

| View | Mean Expected Score | Mean All-Pair Score | Expected Avg Rank | p(score >= observed) | p(rank <= observed) | Expected Ranks |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `feature_similarity` | `0.271292` | `0.173198` | `7.333333` | `0.007143` | `0.038095` | Hermes/Mistral: 1, DeepSeek/Qwen: 2, GLM/Nemotron: 19 |
| `angle_fidelity` | `0.265075` | `0.034532` | `11.333333` | `0.107143` | `0.238095` | Hermes/Mistral: 1, DeepSeek/Qwen: 11, GLM/Nemotron: 22 |
| `amplitude_fidelity` | `0.735052` | `0.639287` | `11.0` | `0.140476` | `0.235714` | Hermes/Mistral: 1, DeepSeek/Qwen: 12, GLM/Nemotron: 20 |

## Binary kNN Sweep

| k | Edge Count | Expected Pair Edges | Null Mean | p(edges >= observed) |
| ---: | ---: | --- | ---: | ---: |
| `1` | `6` | `2/3` | `0.642857` | `0.12381` |
| `2` | `12` | `2/3` | `1.285714` | `0.380952` |
| `3` | `16` | `2/3` | `1.714286` | `0.609524` |
| `4` | `21` | `3/3` | `2.25` | `0.4` |

## Boundary

This strengthens the AI-side feature graph read. It is not a real pathway, molecular, allostery, or attention-flow graph validation until domain-correct graph edges and labels are supplied.
