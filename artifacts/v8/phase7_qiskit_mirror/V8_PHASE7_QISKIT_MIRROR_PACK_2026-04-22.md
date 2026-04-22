# V8 Phase 7 Qiskit Mirror Pack

Date: `2026-04-22`

## Objective

Phase 7 mirrors the completed `Phase 6` PennyLane encoding inside `Qiskit` using the same locked feature vectors.

The purpose is cross-framework simulator lock. This is still not the Bell-type semantic contextuality claim.

## Source

- `Phase 6`: normalized `Phase 3 + Phase 4 + Phase 5` feature vectors
- `Qiskit`: statevector simulation for the same angle and amplitude encodings

## Circuits Mirrored

- `AngleEmbedding mirror`: `RY(feature * pi)` over 12 qubits plus ring CNOT entanglement
- `AmplitudeEmbedding mirror`: normalized 16-amplitude state over 4 qubits plus CNOT chain entanglement

## Cross-Framework Lock

- max absolute AngleEmbedding fidelity delta vs PennyLane: `0.000000000000`
- max absolute AmplitudeEmbedding fidelity delta vs PennyLane: `0.000000000000`

## First Read

The Qiskit mirror locks the Phase 6 handoff: both mirrored circuits reproduce the PennyLane fidelity structure to numerical precision. `Mistral / Hermes` remains the nearest encoded pair in both Qiskit encodings, so the family/bridge signal is not trapped in the PennyLane implementation.

## Qiskit Angle Nearest Pairs

- `Mistral / Hermes`: `0.795224`
- `Mistral / Qwen`: `0.082423`
- `Hermes / GLM`: `0.029426`
- `Mistral / GLM`: `0.027760`
- `Nemotron / SmolLM3`: `0.026543`
- `Mistral / Gemma`: `0.003173`
- `Qwen / GLM`: `0.002178`
- `Gemma / GLM`: `0.000161`

## Qiskit Amplitude Nearest Pairs

- `Mistral / Hermes`: `0.985451`
- `Mistral / GLM`: `0.831179`
- `Hermes / GLM`: `0.816152`
- `Qwen / Gemma`: `0.810588`
- `Mistral / Qwen`: `0.806815`
- `Nemotron / SmolLM3`: `0.784779`
- `Qwen / GLM`: `0.760397`
- `DeepSeek / Nemotron`: `0.747747`

## Charts

- [`Qiskit angle fidelity`](./charts/v8_phase7_qiskit_angle_fidelity_2026-04-22.png)
- [`Qiskit amplitude fidelity`](./charts/v8_phase7_qiskit_amplitude_fidelity_2026-04-22.png)
- [`Angle delta vs PennyLane`](./charts/v8_phase7_angle_delta_vs_pennylane_2026-04-22.png)
- [`Amplitude delta vs PennyLane`](./charts/v8_phase7_amplitude_delta_vs_pennylane_2026-04-22.png)
- [`Qiskit angle expectations`](./charts/v8_phase7_qiskit_angle_expectations_2026-04-22.png)
- [`Qiskit amplitude expectations`](./charts/v8_phase7_qiskit_amplitude_expectations_2026-04-22.png)

## Next

The next clean rung is Bell-state calibration: validate the measurement and observable path before any Bell-type semantic contextuality scoring.
