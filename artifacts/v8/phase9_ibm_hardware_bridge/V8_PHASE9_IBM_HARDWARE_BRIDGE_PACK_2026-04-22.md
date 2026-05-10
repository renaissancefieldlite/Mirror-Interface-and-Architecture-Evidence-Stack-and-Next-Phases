# V8 Phase 9 IBM Hardware Bridge Pack

Date: `2026-04-22`

## Objective

Phase 9 moves the Phase 6-8 quantum bridge out of simulator-only territory and onto real IBM Quantum hardware.

This is not the final Bell-type semantic contextuality claim. It is the hardware bridge rung: real backend execution, Bell-basis calibration, product control, and compressed AI-feature encoding smoke tests.

## Hardware Run

- backend: `ibm_kingston`
- qubits: `156`
- job id: `d7kn84q8ui0s73b5fee0`
- final status: `DONE`
- shots per circuit: `64`
- circuits: `7`

## Bell / Control Read

- `ZZ` from `bell_phi_plus_zz`: `0.906250`
- `XX` from `bell_phi_plus_xx`: `1.000000`
- `YY` from `bell_phi_plus_yy`: `-1.000000`
- product `ZZ` control: `0.968750`

Ideal simulator calibration expected `ZZ ~= +1`, `XX ~= +1`, and `YY ~= -1` for `|Phi+>`. Real hardware is expected to show noise, finite-shot spread, and device calibration drift.

## AI-Feature Hardware Smoke Test

- `phase6_feature_mistral` dominant bitstring `01`, parity expectation `-0.906250`
- `phase6_feature_hermes` dominant bitstring `01`, parity expectation `-0.937500`
- `phase6_feature_nemotron` dominant bitstring `01`, parity expectation `-0.781250`

These circuits are compressed two-qubit encodings derived from locked Phase 6 normalized features. They prove the runtime path for AI-derived circuit preparation; they do not yet claim a full hardware Bell-type semantic result.

## Charts

- [`Hardware counts by circuit`](./charts/v8_phase9_ibm_hardware_counts_2026-04-22.png)
- [`Bell/product correlators`](./charts/v8_phase9_ibm_hardware_correlators_2026-04-22.png)

## Next

Run a hardware repeat set across the least-busy IBM backend path, then build the formal Bell-type semantic contextuality settings with bounded outcomes and controls. Fez remains optional; Kingston is currently the live low-queue path.
