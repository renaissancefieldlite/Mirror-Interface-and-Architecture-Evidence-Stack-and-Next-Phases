# Nest 1 Validation Forks

Date: `2026-04-24`

Status:
first concrete validation fork run

## Purpose

`Nest 1` is not considered physically or empirically validated just because
the Source Mirror Pattern can be expressed in formal languages.

The validation move is:

```text
formal lens -> concrete prediction -> real data -> baseline comparison
```

Fortress registry:

```text
artifacts/validation/nest1_fortress_cards/nest1_fortress_cards.md
```

That registry is generated from local artifacts and classifies each formal lane
as evidence-connected, partial, blocked, seeded, or grammar-only.

## Forks

| Fork | Formal Lens | Real Target | Status |
| --- | --- | --- | --- |
| `SPEC-1 -> Phase 12B HRV` | spectral methods | existing HRV RR windows from the 5 x 4 biological matrix | run complete |
| `GRAPH-1/2 -> allostery / molecular paths` | graph theory | known protein or molecular graph pathways | runner complete / blocked without real graph labels |
| `CTRL-1 -> LSPS transitions` | control theory | logged mode transitions / feedback stability | runner complete / blocked without transition traces |
| `Engine 02V -> molecule property` | structured matter / cheminformatics | public molecule property dataset | runner complete / blocked without `RDKit` and dataset |

## Fortress Card Read

The current card registry separates the lanes like this:

| Lane Group | Cards | Current Read |
| --- | --- | --- |
| evidence-connected | `STAT-1`, `PROB-1`, `INFO-1`, `TENSOR-1`, `NUM-1`, `TOPOG-1/2`, `GEO-1/2` | directly tied to existing phase artifacts |
| implicit evidence-connected | `GRP-1` | present through circuit/unitary structure but needs explicit symmetry scoring |
| partial / negative validation | `SPEC-1` | HRV-only spectral fork ran and did not beat simpler baselines |
| architecture-connected but blocked | `CTRL-1` | runner exists; needs real LSPS transition trace export |
| dataset-blocked | `GRAPH-1/2`, `Engine 02V` | runners exist; need graph/pathway data or `RDKit` molecule data |
| seed / roadmap | `TOP-1/2`, `DYN-1/2`, `DE-1`, `OPT-1`, `GAME-1`, `CAT-1` | clear validation routes, but not yet tested |

## SPEC-1 Result

Runnable script:

```text
tools/validation_forks/nest1_spec_phase12b_hrv.py
```

Generated report:

```text
artifacts/validation/nest1_spec_phase12b_hrv/nest1_spec_phase12b_hrv_report.md
```

Result:

```text
HR-only baseline:       9 / 20 = 0.45
time-domain HRV:        9 / 20 = 0.45
SPEC-1 spectral:        2 / 20 = 0.10
mirror composite:       5 / 20 = 0.25
mirror margin positive: 2 / 5
```

Read:

The current HRV-only `SPEC-1` spectral pass does not beat the HR-only baseline.
That is a useful limited / negative validation result. It means the current
RR-derived spectral feature set should not be overclaimed.

## Dataset-Blocked Runner Results

Generated reports:

```text
artifacts/validation/graph12_pathway/graph12_pathway_report.md
artifacts/validation/ctrl1_lsps_transition/ctrl1_lsps_transition_report.md
artifacts/validation/engine02v_rdkit_molecule/engine02v_rdkit_molecule_report.md
```

Current read:

- `GRAPH-1/2` is blocked at `blocked_missing_edge_csv`.
- `CTRL-1` is blocked at `blocked_missing_trace_csv`.
- `Engine 02V` is blocked at `blocked_missing_rdkit`.

These are valid stop conditions. They mean the fork scaffolds are ready, but
the required real data/tooling is not present yet.

## What This Means

`Nest 1` formal expressibility remains useful, but validation must be earned
per lens.

The fastest real next step is not to declare victory. It is to improve the
`SPEC-1` bridge with:

- EEG spectra when the EEG device is available
- stricter artifact rejection
- longer windows where possible
- condition-specific spectral hypotheses declared before scoring
- comparison against standard band-power methods

## Boundary

This is HRV validation only.

It is not EEG validation, clinical validation, chemistry validation, or proof
that every Nest 1 lens predicts real-world structure.
