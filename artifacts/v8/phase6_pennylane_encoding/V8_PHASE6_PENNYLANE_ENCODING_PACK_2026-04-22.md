# V8 Phase 6 PennyLane Encoding Pack

Date: `2026-04-22`

## Objective

Phase 6 starts the quantum-bridge ladder by turning locked `Phase 3 + Phase 4 + Phase 5` geometry into normalized feature vectors and running first-pass PennyLane encodings.

This is not the Bell-type claim yet. It is the encoding-discovery rung.

## Inputs

- `Phase 3`: peak percentile, band width, target/last magnitude, dimension overlap context
- `Phase 4`: token-path localization and anchor behavior
- `Phase 5`: context-to-readout bridge features and overlap measures

## Feature Vector

- `peak_percentile`
- `band_width`
- `target_peak`
- `last_peak`
- `phase3_last_to_target`
- `target_to_context`
- `target_to_surround`
- `phase5_last_to_target`
- `anchor_layer_span`
- `overlap_count`
- `overlap_jaccard`
- `dominant_anchor_code`

## Encodings Run

- `AngleEmbedding`: 12-wire circuit using normalized feature rotations and ring entanglement
- `AmplitudeEmbedding`: 4-wire compressed state using the same vector padded to 16 amplitudes

## First Read

The first encoding-discovery pass is valid: all eight locked V8 rows are converted into a normalized quantum-bridge feature vector, and both `AngleEmbedding` and `AmplitudeEmbedding` produce comparable state spaces. This gives Phase 7 a concrete Qiskit mirror target instead of a rhetorical handoff.

## Angle-Encoding Nearest Pairs

- `Mistral / Hermes`: `0.795224`
- `Mistral / Qwen`: `0.082423`
- `Hermes / GLM`: `0.029426`
- `Mistral / GLM`: `0.027760`
- `Nemotron / SmolLM3`: `0.026543`
- `Mistral / Gemma`: `0.003173`
- `Qwen / GLM`: `0.002178`
- `Gemma / GLM`: `0.000161`

## Amplitude-Encoding Nearest Pairs

- `Mistral / Hermes`: `0.985451`
- `Mistral / GLM`: `0.831179`
- `Hermes / GLM`: `0.816152`
- `Qwen / Gemma`: `0.810588`
- `Mistral / Qwen`: `0.806815`
- `Nemotron / SmolLM3`: `0.784779`
- `Qwen / GLM`: `0.760397`
- `DeepSeek / Nemotron`: `0.747747`

## Charts

- [`normalized feature heatmap`](./charts/v8_phase6_normalized_feature_heatmap_2026-04-22.png)
- [`feature PCA map`](./charts/v8_phase6_feature_pca_map_2026-04-22.png)
- [`AngleEmbedding fidelity`](./charts/v8_phase6_angle_fidelity_2026-04-22.png)
- [`AmplitudeEmbedding fidelity`](./charts/v8_phase6_amplitude_fidelity_2026-04-22.png)
- [`AngleEmbedding expectations`](./charts/v8_phase6_angle_expectations_2026-04-22.png)
- [`AmplitudeEmbedding expectations`](./charts/v8_phase6_amplitude_expectations_2026-04-22.png)

## Next

The next clean rung is `Phase 7`: mirror the best encoding in `Qiskit`, then compare whether the same family/bridge structure survives outside PennyLane.
