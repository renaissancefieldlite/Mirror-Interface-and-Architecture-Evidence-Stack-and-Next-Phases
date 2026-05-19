# Nest 2 / Nest 3 EPA PM2.5 Atmospheric Particle-State Proxy

Status: `public_safe_support_read / local_ready_unpushed`

## Front-Center Read

The smoke / PM2.5 atmospheric proxy gate is now seated through official EPA
AirData PM2.5 monitor rows with ozone, precursor-gas, and meteorology context.

This row measures particle-state support. PM2.5 is the aerosol-burden surface;
wildfire / smoke source attribution remains the next join using HMS smoke,
fire-perimeter, satellite aerosol, or plume-context data.

Current support level: atmospheric particle-state recovery above geo/season
baseline and shuffled-label controls. This row strengthens oxygen / redox,
environmental fate, Nest 3 atmospheric dynamics, and Nest 5 convergence routing
beside ozone and ozone precursor / meteorology.

## Sources

- EPA AirData daily PM2.5 FRM/FEM mass: `daily_88101_2025.zip`
- EPA AirData daily ozone: `daily_44201_2025.zip`
- EPA AirData daily NO2, CO, SO2, temperature, wind, pressure, relative humidity, and dewpoint context files

## Target QA

- support rows with PM2.5 + ozone + NO2 + temperature + wind context: `69,403`
- PM2.5 monitor sites: `442`
- counties: `111`
- states / territories: `38`
- date range: `2025-01-01` to `2025-10-30`
- high-PM2.5 AQI `>= 51` rows: `20,476`
- shuffled controls per read: `250`

## Context Coverage

| Context source | County-day rows |
| --- | ---: |
| `ozone` | `152,881` |
| `so2` | `58,122` |
| `wind_dir` | `68,869` |
| `wind_speed` | `68,761` |
| `temp` | `86,460` |
| `rh` | `51,530` |
| `no2` | `51,159` |
| `press` | `42,184` |
| `co8` | `28,422` |
| `dewpoint` | `3,967` |

## State Map

| Variable | PM2.5 / smoke-proxy expression |
| --- | --- |
| `state` | PM2.5 ug/m3 and official high-PM2.5 AQI `>= 51` class |
| `control` | shuffled PM2.5 values and shuffled high-PM2.5 labels under fixed splits |
| `transform` | ozone, NO2, CO, SO2, temperature, wind, pressure, humidity, season, event type, and lag context -> particle-state recovery |
| `drift` | seasonal particle loading, meteorological movement, same-site lag movement, and event-type flags |
| `quality` | official EPA monitor rows, observation-percent gate, physical concentration gate, county-day context coverage |
| `support` | particle-context recovery above geo/season baseline and shuffled controls |

## PM2.5 Regression Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `geo_season_site_holdout` | `12` | `52,913` | `16,490` | `0.318078` | `0.100768` | `5.734622` | `6.047542` | `0.003984` |
| `particle_context_site_holdout` | `57` | `52,913` | `16,490` | `0.460728` | `0.209749` | `5.375903` | `6.047542` | `0.003984` |
| `particle_context_lag_temporal` | `63` | `48,221` | `20,373` | `0.596519` | `0.229788` | `5.436765` | `6.327623` | `0.003984` |

## High-PM2.5 AQI Classification Results

| Mode | Features | Train | Test | ROC AUC | AP | Balanced Acc | Macro F1 | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `geo_season_site_holdout` | `12` | `52,913` | `16,490` | `0.698159` | `0.465326` | `0.640048` | `0.604556` | `0.003984` |
| `particle_context_site_holdout` | `57` | `52,913` | `16,490` | `0.789010` | `0.619138` | `0.716611` | `0.691718` | `0.003984` |
| `particle_context_lag_temporal` | `63` | `48,221` | `20,373` | `0.850927` | `0.769182` | `0.730729` | `0.680074` | `0.003984` |

## Read

The clean support read is:

```text
site-heldout particle context:
  PM2.5 Pearson        0.460728
  high-PM2.5 AUC       0.789010
  p                    0.003984

temporal context + lag:
  PM2.5 Pearson        0.596519
  high-PM2.5 AUC       0.850927
  p                    0.003984
```

This seats a PM2.5 atmospheric particle-state row. It complements EPA ozone:
ozone seats oxidant state; ozone precursor / meteorology seats gas + weather
context; PM2.5 seats aerosol burden and high-particle air-quality state.

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | oxygen/redox and environmental fate gain PM2.5 particle-state support |
| `Nest 3` | atmospheric dynamics gain particle-state, gas-context, and meteorology recovery |
| `Nest 4` | biology-facing air-quality interpretation gains a measured particle exposure precursor |
| `Nest 5` | convergence routing can separate ozone, ozone precursor / meteorology, PM2.5, ORP, dissolved oxygen, and water transport rows |
| `FIG.14` | external adapter lane gains EPA AirData particle-monitor examples |
| `FIG.15` | support-state routing gains a smoke / PM2.5 proxy row before attribution joins |

## Next Gate

```text
EPA PM2.5 particle-state proxy seated
-> HMS smoke / fire-perimeter / satellite aerosol attribution join
-> ozone + PM2.5 multi-pollutant environmental-state matrix
```
