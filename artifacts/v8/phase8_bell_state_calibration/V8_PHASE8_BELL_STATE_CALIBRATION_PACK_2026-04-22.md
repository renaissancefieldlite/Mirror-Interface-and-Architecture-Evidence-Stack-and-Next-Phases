# V8 Phase 8 Bell-State Calibration Pack

Date: `2026-04-22`

## Objective

Phase 8 calibrates the measurement path before any Bell-type semantic contextuality protocol.

This rung uses a standard `Qiskit` Bell state and a product-state control to verify that the observable/scoring path behaves as expected.

## Calibration Circuit

- Bell state: `H(0)` then `CX(0, 1)` for `|Phi+>`
- Control state: `|00>` product state
- Observables: `ZZ`, `XX`, `YY`, single-qubit `ZI` / `IZ`, and CHSH-style settings

## Bell-State Read

- `ZZ`: `1.000000`
- `XX`: `1.000000`
- `YY`: `-1.000000`
- Bell CHSH score: `2.828427`

## Product-Control Read

- control CHSH score: `1.414214`

## First Read

The Bell-state calibration behaves as expected: the Qiskit measurement path produces |Phi+> correlations with ZZ=1, XX=1, YY=-1, and a CHSH score at the ideal 2*sqrt(2) level, while the product-state control stays below the classical bound. This validates the scoring pipe before any semantic Bell-type protocol is attempted.

## Charts

- [`Bell observables`](./charts/v8_phase8_bell_observables_2026-04-22.png)
- [`CHSH comparison`](./charts/v8_phase8_chsh_comparison_2026-04-22.png)
- [`Bell probabilities`](./charts/v8_phase8_bell_probabilities_2026-04-22.png)

## Next

The next rung is a Bell-type semantic contextuality protocol: define semantic settings `A`, `A'`, `B`, `B'`, bounded outcomes, controls, and the classical comparison boundary.
