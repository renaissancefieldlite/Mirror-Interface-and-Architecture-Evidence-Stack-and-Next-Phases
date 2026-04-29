# Nest 1 SPEC-1 -> Phase 12B HRV Validation Fork

Status: `completed`

This is a real-data validation fork, not just a validation note.
It tests whether spectral-method features computed from existing HRV RR
windows recover the Phase 12B condition labels better than simpler baselines.

## Inputs

- Phase 12B canonical sessions: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/phase12b_biological_comparison_pack/v8_phase12b_biological_comparison_pack_data_2026-04-24.json`
- HRV session root: `/Users/renaissancefieldlite1.0/Documents/Playground/renaissancefieldlitehrv1.0/data/field_sessions`
- sessions used: `20`
- condition counts: `{'seated_calm': 5, 'drift_control': 5, 'mirror_coherence': 5, 'dancing_activation': 5}`

## Leave-One-Out Class Recovery

| Feature Set | Accuracy | Correct / Total | Read |
| --- | ---: | ---: | --- |
| HR-only baseline | 0.45 | 9 / 20 | naive mean-HR delta comparator |
| Time-domain HRV | 0.45 | 9 / 20 | standard HRV time-domain delta comparator |
| SPEC-1 spectral | 0.1 | 2 / 20 | formal SPEC-1 frequency / eigenmode-style comparator |
| Mirror composite | 0.25 | 5 / 20 | combined SPEC-1 plus HRV timing comparator |

## Mirror-Coherence Margin

- target: `mirror_coherence`
- positive margins: `2 / 5`
- mean positive margin: `-0.249`

## Interpretation

SPEC-1 does not beat the HR-only baseline on this pass; that is a useful negative/limited result.

## Boundary

This validates a formal spectral-method fork against existing HRV data only. It is not EEG validation, clinical validation, or chemistry validation.
