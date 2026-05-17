# Nest 2 Electrochemistry / Redox NASA Battery Support Read

Date: `2026-05-16`

Status: `public_safe_aggregate / real_nasa_dataset / no_raw_rows_published / no_code`

## Purpose

This pass seats the first Electrochemistry / Redox real-data lane after the
H2O, Minerals, and Materials band-gap passes. It uses real NASA Li-ion battery
aging data to map capacity fade, impedance, charge-transfer resistance, and
degraded-state separation.

## Source

- Source: NASA PCoE Battery Data Set
- Public repository: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
- Dataset: `5. Battery Data Set`
- Battery count parsed: `34`
- Discharge rows parsed: `2,794`
- Impedance / EIS rows parsed: `1,956`
- Shuffled controls: `250`

NASA describes this battery set as Li-ion cells run through charge, discharge,
and impedance profiles. The impedance measurements use electrochemical
impedance spectroscopy from `0.1 Hz` to `5 kHz`, and repeated cycles track
accelerated aging until end-of-life capacity fade.

## State Map

| Variable | Electrochemistry expression |
| --- | --- |
| `state` | capacity, state-of-health, EIS Re/Rct, impedance spectra |
| `control` | shuffled capacity values and shuffled degraded-state labels |
| `transform` | voltage / current / temperature / EIS windows -> health or degradation readout |
| `drift` | cycle aging, capacity fade, resistance growth, temperature/load variation |
| `quality` | real NASA battery cycles with linked discharge and impedance rows |
| `support` | held-out battery/group split metrics against shuffled controls |

## Discharge Capacity Recovery

- target: `capacity_ahr`
- rows: `2,769`
- Pearson: `0.923872`
- R2: `0.833991`
- RMSE: `0.187077`
- baseline RMSE: `0.463353`
- RMSE improvement: `0.276275`
- shuffled abs Pearson mean: `0.025824`
- shuffled abs Pearson p95: `0.066936`
- p(Pearson >= real): `0.003984`

Read:

```text
Discharge voltage/current/temperature windows recover capacity fade strongly
above shuffled controls. The p-value is at the 250-permutation floor.
```

## EIS / Impedance Degraded-State Classifier

- target: `nearest_below_80pct_initial`
- rows: `1,956`
- positives: `639`
- controls: `1,317`
- ROC AUC: `0.709188`
- average precision: `0.407440`
- accuracy: `0.673913`
- shuffled AUC mean: `0.499628`
- shuffled AUC p95: `0.566842`
- p(AUC >= real): `0.003984`
- p(AP >= real): `0.071713`
- p(accuracy >= real): `0.115538`

Read:

```text
EIS / impedance rows separate degraded-state labels by ROC AUC above shuffled
controls. AP and accuracy are weaker first-pass metrics, so the support read is
AUC-first and flagged for an impedance-specific follow-up.
```

## EIS / Impedance Continuous Capacity Boundary

- target: `nearest_soh_initial`
- rows: `1,944`
- Pearson: `0.003982`
- R2: `-2.407708`
- RMSE improvement: `-2.630089`
- p(Pearson >= real): `0.928287`

Boundary:

```text
The first grouped EIS-only continuous-capacity regression lands as a boundary
row. EIS is currently seated as a degraded-state classifier and impedance-drift
lane, while continuous EIS-to-SOH regression moves to the follow-up gate.
```

## Meta Analysis

The same p-value floor seen in the band-gap pass appears again on the strongest
NASA battery metrics:

- discharge capacity Pearson p: `0.003984`
- EIS degraded-state ROC AUC p: `0.003984`

That means the real signal beat all `250` shuffled comparators for those
metrics. The electrochemistry lane therefore contributes two support surfaces:
one strong discharge-capacity health read and one impedance/EIS degraded-state
read. The continuous EIS capacity read is the live boundary that keeps the
public claim disciplined.

## Cross-Nest Role

- `Nest 2`: seats Electrochemistry / Redox as a real-data lane.
- `Nest 3`: strengthens impedance / EIS as a physical waveform / frequency
  response branch.
- `Nest 4`: connects battery / impedance logic to future B.A.S.I.S. sensor and
  physiology-state adapters.
- `Nest 5`: adds another support-state card for convergence routing and
  evidence-memory.

## Public / Private Boundary

Public-safe: aggregate source identity, row counts, metrics, state map, support
read, and continuation gates.

Private: downloaded NASA archives, parsed aggregate row tables, runnable
scripts, and local workbench outputs.

## Next Gate

```text
NASA battery aging seated
-> update Nest 5 / Lattice / claim-support pointers
-> build impedance / EIS visual card
-> run RedPred / SOMAS or DUCK/CV molecule redox follow-up
```
