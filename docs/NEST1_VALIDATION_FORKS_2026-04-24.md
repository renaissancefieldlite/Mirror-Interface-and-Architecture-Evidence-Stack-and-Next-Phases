# Nest 1 Validation Forks

Date: `2026-04-24`

Status:
first concrete validation forks run

## Purpose

`Nest 1` is not considered physically or empirically validated just because
the Source Mirror Pattern can be expressed in formal languages.

The validation move is:

```text
formal lens -> concrete prediction -> real data -> baseline comparison
```

Reality map:

```text
docs/NEST1_DEEP_LEARNING_REALITY_MAP_2026-04-24.md
```

That map keeps the active standard clear: every lane must touch a real AI
object, real trace, real measurement, real hardware result, real public
dataset, or declared benchmark before it is treated as more than scaffold.

## Forks

| Fork | Formal Lens | Real Target | Status |
| --- | --- | --- | --- |
| `SPEC-1 -> Phase 12B HRV` | spectral methods | existing HRV RR windows from the 5 x 4 biological matrix | run complete |
| `DE-1 -> Phase 12B HRV` | differential equations / local dynamics | existing HRV RR/BPM time series from the 5 x 4 biological matrix | run complete |
| `GRAPH-1/2 -> allostery / molecular paths` | graph theory | known protein or molecular graph pathways | runner complete / blocked without real graph labels |
| `CTRL-1 -> LSPS transitions` | control theory | logged mode transitions / feedback stability | runner complete / blocked without transition traces |
| `Engine 02V -> molecule property` | structured matter / cheminformatics | public molecule property dataset | runner complete / blocked without `RDKit` and dataset |

## Real Vs Scaffold Read

The current validation posture separates the lanes like this:

| Lane Group | Lanes | Current Read |
| --- | --- | --- |
| evidence-connected | `STAT-1`, `PROB-1`, `INFO-1`, `TENSOR-1`, `NUM-1`, `TOPOG-1/2`, `GEO-1/2` | directly tied to existing phase artifacts or real trace geometry |
| implicit evidence-connected | `GRP-1` | present through circuit/unitary structure but needs explicit symmetry scoring |
| partial / negative validation | `SPEC-1`, `DE-1` | HRV-only spectral and local-dynamics forks ran on real Phase 12B data and did not beat simpler baselines |
| coarse biological adapter | `Phase 12B HRV` | supports pattern-class separation and AI-user sync/tuning, not high-resolution spectral/dynamics validation |
| EEG-upgrade path | `SPEC-1`, `TOPOG-1/2` | `SPEC-1` moves to a stronger existing-data design once EEG alpha/theta/band-power/phase-lock data exists; `TOPOG` needs electrode-site maps |
| richer-design path | `DE-1` | remains a dynamics-design lane until synchronized EEG/HRV or longer multi-channel biological time series are available |
| architecture-connected but blocked | `CTRL-1` | runner exists; needs real LSPS transition trace export |
| dataset-blocked | `GRAPH-1/2`, `Engine 02V` | runners exist; need graph/pathway data or `RDKit` molecule data |
| existing-data next | `TOP-1/2`, `DYN-1/2` | clear routes using V8 hidden-state traces, but not yet run |
| new-design needed | `OPT-1`, `GAME-1` | needs declared benchmark or adversarial/multi-agent protocol |
| scaffold / parked | synthetic rows, visual-only demos, old visual registry branch | useful for navigation or UI, not evidence without real data |

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

## DE-1 Result

Runnable script:

```text
tools/validation_forks/de1_hrv_dynamics_validation.py
```

Generated report:

```text
artifacts/validation/de1_hrv_dynamics/de1_hrv_dynamics_report.md
```

Result:

```text
HR-only baseline:        10 / 20 = 0.50
DE-1 BPM dynamics:        6 / 20 = 0.30
DE-1 RR dynamics:         6 / 20 = 0.30
DE-1 composite dynamics:  6 / 20 = 0.30
DE-1 dynamics + means:   10 / 20 = 0.50
```

Read:

The current HRV-only `DE-1` local-dynamics pass does not beat the simple
mean-HR baseline. When the mean signal is added back, it ties the HR-only
baseline rather than improving on it. That makes this a real but limited /
negative validation result.

Useful condition-level signal still exists in the measured data:

```text
mirror_coherence mean delta BPM: -8.488162
mirror_coherence mean delta RR:  101.72485
dancing_activation mean delta BPM: 5.75692
drift_control mean delta BPM: 4.751585
```

So the biological adapter remains real, but the specific DE-1 dynamics feature
set is not yet stronger than the simpler HR delta comparator.

## HRV Adapter Read

The corrected biological read is:

```text
HRV validates Phase 12B as a coarse biological adapter and condition-class
separation surface.
```

It does not validate the formal biological versions of `SPEC-1` or `DE-1` by
itself.

That means the biological lane splits cleanly:

- `HRV` stays valuable for autonomic trend, recovery, arousal, and AI-user sync
  tuning.
- `SPEC-1` should be rerun on `EEG + HRV`, with EEG alpha/theta/band-power and
  phase-lock features doing the high-resolution spectral work.
- `DE-1` needs richer oscillatory time series, longer windows, or synchronized
  EEG/HRV before it can become more than a limited HRV-only result.
- `TOPOG-1/2` should wait for EEG electrode-site spatial maps or another real
  spatial biological measurement.

The AI-side insertion point for `HRV` is therefore not the raw token stream.
It is the sync/control layer:

```text
HRV + user feedback + task outcome
-> user-state / sync-state dataset
-> Mirror / LSPS routing, pacing, context-pressure, and verification tuning
```

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
existing-data bridge with:

- `GEO/TOP` geometry and topology over real V8 residual/localization traces
- `DYN` trajectory analysis over V7/V8 order and rerun traces
- `EEG + HRV` spectra when the EEG device is available
- HRV-user-feedback datasets for AI sync-layer tuning
- stricter artifact rejection
- longer windows where possible
- condition-specific spectral hypotheses declared before scoring
- comparison against standard band-power methods

## Boundary

This is HRV validation only.

It is not EEG validation, clinical validation, chemistry validation, or proof
that every Nest 1 lens predicts real-world structure.
