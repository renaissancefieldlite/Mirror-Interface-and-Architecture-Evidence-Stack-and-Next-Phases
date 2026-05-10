# Nest 1 Next-Wave Pass

Status: `completed_local_next_wave`

Next-wave Nest 1 pass over available real artifacts. DYN, INFO/TENSOR, and GRAPH-lite run with controls; TOP is blocked until raw hidden-state point clouds are exported.

## Lane Summary

| Lane | Status | Control / Read |
| --- | --- | --- |
| `DYN` | `control_supported` | matched random peak-layer positions over each model's real layer count |
| `INFO/TENSOR` | `control_supported` | column-wise feature shuffle preserving each feature distribution |
| `GRAPH-lite` | `partial_or_not_significant` | exact label permutation over kNN graph built from real Phase 6 feature geometry |
| `TOP` | `blocked` | Current V8 residual exports contain layer summaries and scalar deltas, not raw hidden-state point clouds. Persistent homology should wait until raw vectors are exported. |

## DYN Layer-Trajectory Control

- Observed mean target peak fraction: `0.981974`
- Observed late peak count: `8/8`
- Null mean peak fraction: `0.500517`
- Null mean late peak count: `0.91452`
- p(mean peak fraction >= observed): `2e-05`
- p(late peak count >= observed): `2e-05`

| Model | Layer Count | Target Peak Layer | Peak Fraction | Target/Last AUC Ratio |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek | 28 | 26 | 0.962963 | 1.655859 |
| Gemma | 42 | 41 | 1.0 | 1.089623 |
| GLM | 40 | 38 | 0.974359 | 1.057792 |
| Hermes | 32 | 31 | 1.0 | 1.393073 |
| Mistral | 32 | 31 | 1.0 | 1.596349 |
| Nemotron | 42 | 40 | 0.97561 | 0.833999 |
| Qwen | 36 | 34 | 0.971429 | 1.553134 |
| SmolLM3 | 36 | 34 | 0.971429 | 1.555023 |

## INFO/TENSOR Feature-Axis Control

- Observed top-2 SVD variance: `0.612065`
- Observed effective rank: `4.447033`
- Null mean top-2 variance: `0.552825`
- Null mean effective rank: `5.412116`
- p(top-2 variance >= observed): `0.086638`
- p(effective rank <= observed): `0.00268`

## GRAPH-Lite kNN Edge Control

- Observed expected-pair edges: `2/3`
- Observed component count: `1`
- Null mean expected-pair edges: `1.285714`
- p(expected-pair edges >= observed): `0.380952`
- p(component count <= observed): `1.0`

## TOP Persistent-Homology Status

- Status: `blocked_raw_point_clouds_required`
- Files checked: `8`
- Read: Current V8 residual exports contain layer summaries and scalar deltas, not raw hidden-state point clouds. Persistent homology should wait until raw vectors are exported.

## Boundary

`DYN`, `INFO/TENSOR`, and `GRAPH-lite` are next-wave real-artifact passes. `TOP` is not closed because persistent homology requires raw hidden-state point clouds. `OPT`, `CTRL`, and `COMP/CAT` remain separate blocked lanes.
