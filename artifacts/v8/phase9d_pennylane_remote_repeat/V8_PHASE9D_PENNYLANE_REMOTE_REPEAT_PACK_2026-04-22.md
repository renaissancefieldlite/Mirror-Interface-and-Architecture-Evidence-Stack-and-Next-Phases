# V8 Phase 9D PennyLane Remote Hardware Repeat Pack

Date: `2026-04-22`

## Objective

Repeat the direct PennyLane hardware route from Phase 9C across same-backend and cross-backend passes.

This rung tests whether the PennyLane `qiskit.remote` path preserves the Bell/control directions and the compressed AI-feature parity direction under live IBM hardware noise.

## Hardware Route

- device: `qml.device('qiskit.remote')`
- PennyLane: `0.44.1`
- PennyLane-Qiskit: `0.44.1`
- shots per circuit: `64`
- repeat passes: `3`

## Bell / Control Repeat Read

- `1-fez-baseline` on `ibm_fez`: bell_phi_plus_zz=0.843750 dom 00; bell_phi_plus_xx=0.968750 dom 11; bell_phi_plus_yy=-0.843750 dom 01; product_00_zz=0.906250 dom 00
- `2-fez-repeat` on `ibm_fez`: bell_phi_plus_zz=0.968750 dom 11; bell_phi_plus_xx=0.968750 dom 00; bell_phi_plus_yy=-0.906250 dom 01; product_00_zz=0.937500 dom 00
- `3-kingston-repeat` on `ibm_kingston`: bell_phi_plus_zz=0.968750 dom 11; bell_phi_plus_xx=1.000000 dom 11; bell_phi_plus_yy=-0.937500 dom 10; product_00_zz=0.937500 dom 00

## Compressed AI-Feature Repeat Read

- `1-fez-baseline` on `ibm_fez`: phase6_feature_mistral=-0.625000 dom 10; phase6_feature_hermes=-0.531250 dom 10; phase6_feature_nemotron=-0.718750 dom 10
- `2-fez-repeat` on `ibm_fez`: phase6_feature_mistral=-0.687500 dom 10; phase6_feature_hermes=-0.625000 dom 10; phase6_feature_nemotron=-0.812500 dom 10
- `3-kingston-repeat` on `ibm_kingston`: phase6_feature_mistral=-0.750000 dom 10; phase6_feature_hermes=-0.875000 dom 10; phase6_feature_nemotron=-0.468750 dom 10

## First Read

Phase 9D repeats the direct PennyLane hardware path with Phase 9C as baseline. The primary comparison is parity direction because dominant bitstrings can flip under wire/classical-bit ordering conventions.

## Charts

- [`Bell/control PennyLane hardware repeatability`](./charts/v8_phase9d_pennylane_remote_bell_control_repeatability_2026-04-22.png)
- [`AI-feature PennyLane hardware repeatability`](./charts/v8_phase9d_pennylane_remote_feature_repeatability_2026-04-22.png)

## Boundary

This is direct PennyLane hardware repeatability evidence. It is still a bridge rung toward formal Bell-type semantic contextuality, not the final Bell-type claim.
