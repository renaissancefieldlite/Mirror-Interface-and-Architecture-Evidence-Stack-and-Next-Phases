# Nest 2 DUCK/CV + EIS-to-SOH Follow-Up

Status: `public_safe_support_read`

## Front-Center Read

Electrochemistry now has a seated cyclic-voltammetry waveform row.

The earlier electrochemistry branch had battery discharge, EIS degraded-state,
and molecule-level redox support. This pass adds raw cyclic-voltammetry
current-vs-voltage waveform structure through DUCK TL/SDL data, then returns to
the NASA EIS boundary and improves the continuous SOH read by separating
cross-battery generalization from same-battery temporal tracking.

## Sources

- DUCK datasets: <https://doi.org/10.5281/zenodo.18015308>
- DUCK software package: <https://gitlab.com/dgarayr/duck>
- NASA PCoE Battery Data Set: <https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/>

## State Map

| Variable | CV / EIS expression |
| --- | --- |
| `state` | measured current-vs-voltage waveform, peak structure, loop shape, EIS impedance state, SOH |
| `control` | shuffled source, chemistry-family, pH, and SOH labels |
| `transform` | raw I-V trace -> waveform stats, peak features, loop hysteresis, resampled trace vector; EIS features -> SOH read |
| `drift` | scan path, pH, electrolyte family, protocol source, aging cycle, impedance shift |
| `quality` | raw DUCK CV strings from SQLite plus metadata; NASA EIS rows linked to nearest discharge capacity |
| `support` | held-out waveform and EIS tests above shuffled controls |

## DUCK Cyclic-Voltammetry Waveform Gate

Aggregate rows:

- CV rows parsed: `201`
- TL rows: `122`
- SDL rows: `79`
- shuffled controls per test: `250`

### Source / Protocol State Separation

- target: `dataset_binary`
- rows: `201`
- ROC AUC: `1.000000`
- average precision: `1.000000`
- accuracy: `1.000000`
- shuffled AUC mean: `0.500493`
- shuffled AUC p95: `0.623580`
- p(AUC >= real): `0.003984`

### Primary CV Chemistry-Family Waveform Recovery

- target: `primary_redox`
- rows: `190`
- classes: `Ag=14`, `Bi=69`, `Cu=55`, `EDOT=11`, `Ni=8`, `V=33`
- balanced accuracy: `0.906863`
- macro F1: `0.928283`
- accuracy: `0.947368`
- shuffled balanced accuracy mean: `0.173029`
- shuffled balanced accuracy p95: `0.278299`
- p(balanced accuracy >= real): `0.003984`

### pH State Separation

- target: `ph_binary`
- rows: `79`
- ROC AUC: `0.883333`
- average precision: `0.929084`
- accuracy: `0.869565`
- p(AUC >= real): `0.003984`

## Continuous EIS-to-SOH Follow-Up

The original NASA pass seated EIS degraded-state classification and held
continuous EIS-to-SOH regression as the boundary. This follow-up keeps the hard
cross-battery read visible while adding the same-battery temporal tracking
surface.

| Mode | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: |
| `pure_eis_group_holdout` | `0.098518` | `-0.444598` | `3.719985` | `3.095271` | `0.091633` |
| `eis_cycle_context_group_holdout` | `0.376778` | `-2.743321` | `0.922453` | `1.400070` | `0.003984` |
| `eis_cycle_context_same_battery_temporal` | `0.876422` | `0.762003` | `2.149699` | `4.406612` | `0.003984` |

## Read

DUCK/CV adds the missing electrochemical waveform surface. The row moves the
electrochemistry lane from discharge summaries, impedance summaries, and
molecule redox tables into raw I-V waveform structure.

The EIS result is now cleaner:

- cross-battery continuous SOH generalization remains the harder boundary
- EIS + cycle-context already carries a significant support read
- same-battery temporal EIS + cycle-context gives the strongest continuous SOH
  improvement surface

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | electrochemistry / redox lane now includes DUCK/CV waveform support |
| `Nest 3` | waveform / impedance branch strengthened by real I-V and EIS response surfaces |
| `Nest 5` | support-state matrix gains a CV waveform card and a separated SOH boundary/improvement card |
| `FIG.14` | external adapter examples now include battery EIS, molecule redox, and cyclic voltammetry |
| `FIG.15` | Mirror Index / Golden Mirror support-state routing can separate source, chemistry-family, pH, degradation, and SOH tracking reads |

## Next Gate

```text
DUCK/CV seated
-> tighten redox-family / pH / peak-state cards
-> improve continuous EIS-to-SOH with frequency-resolved modeling
-> route CV + EIS into Nest 3 waveform / impedance branch
```
