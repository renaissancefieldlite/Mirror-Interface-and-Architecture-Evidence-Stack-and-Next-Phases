# V8 Phase 9B IBM Hardware Repeatability Pack

Date: `2026-04-22`

## Objective

Phase 9B repeats the Phase 9 hardware bridge on real IBM Quantum backends before moving into formal Bell-type semantic settings.

This keeps the claim boundary clean: hardware runtime path and repeatability first; semantic contextuality protocol later.

## Runs

- `1-kingston` backend `ibm_kingston`, job `d7kn84q8ui0s73b5fee0`, status `DONE`, shots `64`
- `2-kingston` backend `ibm_kingston`, job `d7kovhq8ui0s73b5hf2g`, status `DONE`, shots `64`
- `3-fez` backend `ibm_fez`, job `d7kp0a8e7usc73f53d8g`, status `DONE`, shots `64`

## Bell / Control Repeat Read

- `1-kingston`: ZZ `0.906250`, XX `1.000000`, YY `-1.000000`, product_ZZ `0.968750`
- `2-kingston`: ZZ `0.937500`, XX `0.968750`, YY `-0.906250`, product_ZZ `0.968750`
- `3-fez`: ZZ `0.937500`, XX `0.968750`, YY `-0.750000`, product_ZZ `0.937500`

## AI-Feature Repeat Read

- `1-kingston`: mistral `-0.906250` / dominant `01`; hermes `-0.937500` / dominant `01`; nemotron `-0.781250` / dominant `01`
- `2-kingston`: mistral `-0.750000` / dominant `01`; hermes `-0.718750` / dominant `01`; nemotron `-0.687500` / dominant `01`
- `3-fez`: mistral `-0.781250` / dominant `01`; hermes `-0.656250` / dominant `01`; nemotron `-0.687500` / dominant `01`

## First Read

The IBM hardware bridge repeated successfully. The Bell/control calibration remains directionally aligned across same-backend and cross-backend runs, while compressed Phase 6 AI-feature circuits retain a consistent negative-parity signature with finite-shot and device-level variation.

## Charts

- [`Bell/control repeatability`](./charts/v8_phase9b_bell_control_repeatability_2026-04-22.png)
- [`AI-feature repeatability`](./charts/v8_phase9b_feature_repeatability_2026-04-22.png)

## Next

Use this hardware repeatability rung to justify formal Bell-type semantic contextuality design: explicit `A`, `A'`, `B`, `B'`, bounded outcomes, controls, backend repeats, and public-safe documentation only.
