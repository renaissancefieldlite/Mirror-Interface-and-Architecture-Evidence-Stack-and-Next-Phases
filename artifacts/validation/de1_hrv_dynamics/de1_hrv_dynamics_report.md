# Nest 1 DE-1 -> Phase 12B HRV Dynamics Validation Fork

Status: `completed`

This is a real-data validation fork, not a validation note.
It fits a bounded first-order local dynamics model to actual Phase 12B
BPM and RR windows, then compares condition recovery against a simple
mean-HR delta baseline.

## Inputs

- Phase 12B canonical sessions: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/phase12b_biological_comparison_pack/v8_phase12b_biological_comparison_pack_data_2026-04-24.json`
- HRV session root: `/Users/renaissancefieldlite1.0/Documents/Playground/renaissancefieldlitehrv1.0/data/field_sessions`
- sessions used: `20`
- condition counts: `{'seated_calm': 5, 'drift_control': 5, 'mirror_coherence': 5, 'dancing_activation': 5}`

## Leave-One-Out Class Recovery

| Feature Set | Accuracy | Correct / Total | Read |
| --- | ---: | ---: | --- |
| HR-only baseline | 0.5 | 10 / 20 | naive mean-BPM delta baseline |
| DE-1 BPM dynamics | 0.3 | 6 / 20 | DE-1 local dynamics over BPM only |
| DE-1 RR dynamics | 0.3 | 6 / 20 | DE-1 local dynamics over RR intervals only |
| DE-1 composite dynamics | 0.3 | 6 / 20 | DE-1 local dynamics over BPM plus RR |
| DE-1 dynamics + means | 0.5 | 10 / 20 | DE-1 dynamics plus mean-signal deltas |

## Condition Dynamics Snapshot

| Condition | Runs | Mean delta BPM a | Mean delta BPM | Mean delta RR a | Mean delta RR |
| --- | ---: | ---: | ---: | ---: | ---: |
| dancing_activation | 5 | 0.097307 | 5.75692 | 0.094545 | -50.023915 |
| drift_control | 5 | 0.01475 | 4.751585 | 0.060318 | -49.45432 |
| mirror_coherence | 5 | 0.029919 | -8.488162 | 0.023804 | 101.72485 |
| seated_calm | 5 | 0.036921 | -1.217622 | 0.073076 | 11.985538 |

## Interpretation

DE-1 dynamics does not beat the mean-HR baseline on this pass; that is a useful limited/negative result and prevents overclaiming.

## Boundary

This is a real HRV time-series dynamics validation fork. It is not clinical biology, not EEG, and not a universal biological claim.
