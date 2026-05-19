# Nest 2 / Nest 3 NOAA HMS Smoke + EPA PM2.5 Attribution Join

Status: `public_safe_support_read / local_ready_unpushed`

## Front-Center Read

The PM2.5 atmospheric row now has a NOAA HMS smoke-attribution join. The
previous PM2.5 row seated particle-state recovery; this pass adds real smoke
plume polygons and tests whether monitor-days inside those plumes separate and
improve the particle-state read.

Current support level: NOAA HMS smoke exposure separates PM2.5 state from
non-smoke monitor-days and improves the PM2.5 recovery modes above the
context-only baseline. The lane now carries a real source-attributed aerosol
row for environmental fate, Nest 3 atmospheric dynamics, and Nest 5
convergence routing.

## Sources

- NOAA Hazard Mapping System annual smoke polygon KML: `hms_smoke2025.kml`
- EPA AirData daily PM2.5 FRM/FEM mass: `daily_88101_2025.zip`
- EPA AirData ozone, precursor-gas, and meteorology context files

## Target QA

- PM2.5 support rows after context gate: `69,403`
- PM2.5 monitor sites: `442`
- states / territories: `38`
- date range: `2025-01-01` to `2025-10-30`
- NOAA HMS smoke polygons parsed: `24,238`
- NOAA HMS smoke dates: `366`
- PM2.5 rows under HMS smoke: `16,317`
- PM2.5 sites under HMS smoke: `435`
- shuffled controls per read: `250`

## HMS Density Coverage

| Density | PM2.5 rows |
| --- | ---: |
| `none` | `53,086` |
| `light` | `14,007` |
| `medium` | `1,981` |
| `heavy` | `329` |

## Smoke / Non-Smoke Contrast

| Contrast | Value | p |
| --- | ---: | ---: |
| PM2.5 mean under smoke | `10.855206` |  |
| PM2.5 mean without smoke | `7.052074` |  |
| PM2.5 smoke delta | `3.803132` | `0.003984` |
| High-PM2.5 rate under smoke | `0.493534` |  |
| High-PM2.5 rate without smoke | `0.234017` |  |
| High-PM2.5 smoke-rate delta | `0.259518` | `0.003984` |

## State Map

| Variable | HMS smoke + PM2.5 expression |
| --- | --- |
| `state` | PM2.5 ug/m3, high-PM2.5 AQI class, and NOAA smoke-density exposure |
| `control` | shuffled PM2.5 / AQI labels and shuffled smoke-exposure contrast |
| `transform` | HMS smoke polygon containment + ozone / precursor / meteorology context -> particle-state recovery |
| `drift` | smoke-density class, plume timing, seasonal aerosol transport, same-site lag movement |
| `quality` | official NOAA HMS polygons, official EPA monitor rows, observation-percent gate, point-in-polygon spatial join |
| `support` | HMS-attributed smoke exposure separates particle state and improves source-context routing |

## PM2.5 Regression Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `context_site_holdout` | `57` | `52,913` | `16,490` | `0.460728` | `0.209749` | `5.375903` | `6.047542` | `0.003984` |
| `context_hms_site_holdout` | `66` | `52,913` | `16,490` | `0.486355` | `0.229486` | `5.308344` | `6.047542` | `0.003984` |
| `context_lag_temporal` | `63` | `48,221` | `20,373` | `0.596519` | `0.229788` | `5.436765` | `6.327623` | `0.003984` |
| `context_hms_lag_temporal` | `72` | `48,221` | `20,373` | `0.634498` | `0.346637` | `5.007404` | `6.327623` | `0.003984` |

## High-PM2.5 AQI Classification Results

| Mode | Features | Train | Test | ROC AUC | AP | Balanced Acc | Macro F1 | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `context_site_holdout` | `57` | `52,913` | `16,490` | `0.789010` | `0.619138` | `0.716611` | `0.691718` | `0.003984` |
| `context_hms_site_holdout` | `66` | `52,913` | `16,490` | `0.807164` | `0.646954` | `0.727940` | `0.704589` | `0.003984` |
| `context_lag_temporal` | `63` | `48,221` | `20,373` | `0.850927` | `0.769182` | `0.730729` | `0.680074` | `0.003984` |
| `context_hms_lag_temporal` | `72` | `48,221` | `20,373` | `0.861054` | `0.783012` | `0.756341` | `0.715406` | `0.003984` |

## Read

The clean support read is:

```text
HMS smoke / non-smoke contrast:
  PM2.5 mean delta        +3.803132 ug/m3
  high-PM2.5 rate delta   +0.259518
  p                       0.003984

site-heldout context -> context + HMS:
  PM2.5 Pearson           0.460728 -> 0.486355
  high-PM2.5 AUC          0.789010 -> 0.807164
  p                       0.003984

temporal context + lag -> context + lag + HMS:
  PM2.5 Pearson           0.596519 -> 0.634498
  high-PM2.5 AUC          0.850927 -> 0.861054
  p                       0.003984
```

This seats the smoke-attributed particle-state row. PM2.5 is the measured
aerosol burden; NOAA HMS supplies the real plume-containment source context.

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | environmental fate gains a real smoke-attributed PM2.5 particle-state row |
| `Nest 3` | atmospheric dynamics gain plume containment, particle load, gas context, meteorology, and lag recovery |
| `Nest 4` | biology-facing air-quality interpretation gains a measured smoke / particle exposure precursor |
| `Nest 5` | convergence routing can separate ozone, precursor / meteorology, PM2.5 state, and HMS smoke-attributed PM2.5 |
| `FIG.14` | external adapter lane gains NOAA HMS + EPA AirData joined monitoring examples |
| `FIG.15` | support-state routing gains a source-attribution row before fire-perimeter / satellite aerosol refinement |

## Next Gate

```text
NOAA HMS smoke + EPA PM2.5 attribution seated
-> fire-perimeter / satellite aerosol source refinement
-> ozone + PM2.5 multi-pollutant environmental-state matrix
```
