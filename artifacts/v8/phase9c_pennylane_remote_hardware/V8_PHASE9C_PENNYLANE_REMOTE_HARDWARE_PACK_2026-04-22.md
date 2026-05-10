# V8 Phase 9C PennyLane Remote Hardware Pack

Date: `2026-04-22`

## Objective

Phase 9C runs PennyLane itself against a real IBM Quantum backend using the `pennylane-qiskit` `qiskit.remote` device.

This closes the boundary between Phase 6 PennyLane-local-simulator encoding and Phase 9/9B Qiskit Runtime hardware execution.

## Hardware Run

- PennyLane: `0.44.1`
- PennyLane-Qiskit: `0.44.1`
- backend: `ibm_fez`
- shots per circuit: `64`
- circuits: `7`

## Readout

- `bell_phi_plus_zz` job `d7kp9u24lglc73fvogj0` dominant `00`, parity `0.843750`
- `bell_phi_plus_xx` job `d7kpa0okj84c73ce68ig` dominant `11`, parity `0.968750`
- `bell_phi_plus_yy` job `d7kpa2oe7usc73f53pjg` dominant `01`, parity `-0.843750`
- `product_00_zz` job `d7kpa4a4lglc73fvogqg` dominant `00`, parity `0.906250`
- `phase6_feature_mistral` job `d7kpa6a8ui0s73b5hru0` dominant `10`, parity `-0.625000`
- `phase6_feature_hermes` job `d7kpa8q8ui0s73b5hs20` dominant `10`, parity `-0.531250`
- `phase6_feature_nemotron` job `d7kpasa8ui0s73b5hspg` dominant `10`, parity `-0.718750`

## First Read

PennyLane remote execution successfully ran the bridge circuits on real IBM hardware through the PennyLane-Qiskit device path.

## Charts

- [`PennyLane hardware counts`](./charts/v8_phase9c_pennylane_remote_counts_2026-04-22.png)
- [`PennyLane hardware parity`](./charts/v8_phase9c_pennylane_remote_parity_2026-04-22.png)

## Boundary

This is a direct PennyLane hardware execution rung. It is not yet the formal Bell-type semantic contextuality claim.
