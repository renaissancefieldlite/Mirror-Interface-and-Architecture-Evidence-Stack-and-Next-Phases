# V8 Phase 10 Bell-Type Semantic Contextuality Pack

Date: `2026-04-23`

## Objective

Phase 10 locks the Bell-type semantic contextuality protocol on the compressed AI-feature state layer before hardware repeatability.

The protocol uses the existing `V7` contextuality lane plus the locked `V8 Phase 5` bridge features to define the semantic label buckets `A`, `A'`, `B`, and `B'`, then resolves family-local measurement vectors from the compressed two-qubit correlation matrix.

## Protocol Boundary

- semantic / AI-side contextuality only
- compressed two-qubit feature states derived from locked public-safe summary features
- matched unentangled control uses the same single-qubit rotations with the entangling `CX` removed
- this is not a physical Bell nonlocality claim

## Semantic Setting Buckets

- `A`: lattice / mirror-context setting
- `A'`: matched alternate-context setting
- `B`: target-span bridge setting
- `B'`: readout carry-through setting

## Focused Cohorts

- full semantic overlap cohort: `Mistral`, `Hermes`, `Gemma`, `GLM`, `Nemotron`, `Qwen`, `DeepSeek`
- V8 state-only sidecar: `SmolLM3`

## Aggregate Read

- mean entangled `S_max`: `2.018908`
- mean matched-control `S_max`: `2.000000`
- rows above classical bound: `8 / 8`
- strongest model: `DeepSeek` at `2.040519`
- weakest model: `Gemma` at `2.005572`

## First Read

Phase 10 locks the Bell-type semantic contextuality rung at the compressed state-geometry level. All compressed semantic feature states show `S_max > 2` under resolved family-local measurement settings, while the matched unentangled controls remain exactly at the classical bound. This is a candidate semantic contextuality result on the AI-side feature-state layer, not a physical Bell nonlocality claim. The next step is hardware semantic repeatability with the locked setting map.

## Per-Model Read

- `Mistral` (`full_semantic_overlap`): entangled `S_max` `2.009513`, control `2.000000`, entropy `0.024254`
- `Hermes` (`full_semantic_overlap`): entangled `S_max` `2.009253`, control `2.000000`, entropy `0.023682`
- `Gemma` (`full_semantic_overlap`): entangled `S_max` `2.005572`, control `2.000000`, entropy `0.015262`
- `GLM` (`full_semantic_overlap`): entangled `S_max` `2.019500`, control `2.000000`, entropy `0.044825`
- `Nemotron` (`full_semantic_overlap`): entangled `S_max` `2.011360`, control `2.000000`, entropy `0.028254`
- `Qwen` (`full_semantic_overlap`): entangled `S_max` `2.025713`, control `2.000000`, entropy `0.056659`
- `DeepSeek` (`full_semantic_overlap`): entangled `S_max` `2.040519`, control `2.000000`, entropy `0.083035`
- `SmolLM3` (`v8_state_sidecar`): entangled `S_max` `2.029830`, control `2.000000`, entropy `0.064218`

## Charts

- [`Semantic CHSH vs control`](./charts/v8_phase10_semantic_chsh_vs_control_2026-04-23.png)
- [`Exceedance margin`](./charts/v8_phase10_semantic_exceedance_margin_2026-04-23.png)
- [`Entanglement entropy`](./charts/v8_phase10_semantic_entanglement_entropy_2026-04-23.png)

## Next

The next rung is `Phase 11`: carry the locked Phase 10 semantic settings into real IBM hardware repeatability through both the `Qiskit` and direct `PennyLane` paths.
