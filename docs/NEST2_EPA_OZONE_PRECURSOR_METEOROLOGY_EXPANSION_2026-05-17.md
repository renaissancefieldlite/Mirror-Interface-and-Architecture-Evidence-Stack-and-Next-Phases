# Nest 2 / Nest 3 EPA Ozone Precursor / Meteorology Expansion

Status: `public_safe_support_read / local_ready_unpushed`

## Front-Center Read

The ozone / oxidant-state branch now has a real precursor and meteorology
expansion.

The previous EPA ozone row seated atmospheric oxidant state using official
ozone monitor records. This follow-up adds county-day context from NO2, CO,
SO2, temperature, wind, pressure, relative humidity, and dewpoint. The result
tests whether precursor / meteorology context recovers ozone ppm and AQI
`>= 51` state above shuffled controls.

Current support level: measured atmospheric-state recovery. Precursor gases
and meteorology improve the ozone-state read above shuffled controls, while
peroxide, dissolved oxidant chemistry, wildfire-smoke, and photochemical
mechanism tests remain continuation gates.

## Sources

- EPA AirData daily ozone: <https://aqs.epa.gov/aqsweb/airdata/daily_44201_2025.zip>
- EPA AirData NO2 precursor: <https://aqs.epa.gov/aqsweb/airdata/daily_42602_2025.zip>
- EPA AirData CO gas context: <https://aqs.epa.gov/aqsweb/airdata/daily_42101_2025.zip>
- EPA AirData SO2 gas context: <https://aqs.epa.gov/aqsweb/airdata/daily_42401_2025.zip>
- EPA AirData meteorology: <https://aqs.epa.gov/aqsweb/airdata/daily_TEMP_2025.zip>, <https://aqs.epa.gov/aqsweb/airdata/daily_WIND_2025.zip>, <https://aqs.epa.gov/aqsweb/airdata/daily_PRESS_2025.zip>, <https://aqs.epa.gov/aqsweb/airdata/daily_RH_DP_2025.zip>
- EPA AirData download index: <https://aqs.epa.gov/aqsweb/airdata/download_files.html>

## Target QA

- support rows with NO2 + temperature + wind context: `76,020`
- ozone monitor sites: `390`
- counties: `121`
- states / territories: `39`
- date range: `2025-01-01` to `2025-10-30`
- high-ozone AQI `>= 51` rows: `15,840`
- shuffled controls per read: `250`

## Context Coverage

| Context source | County-day rows |
| --- | ---: |
| `NO2` | `51,159` |
| `CO 8-hour` | `28,422` |
| `SO2` | `58,122` |
| `temperature` | `86,460` |
| `wind speed` | `68,761` |
| `wind direction` | `68,869` |
| `pressure` | `42,184` |
| `relative humidity` | `51,530` |
| `dewpoint` | `3,967` |

## State Map

| Variable | Precursor / meteorology expression |
| --- | --- |
| `state` | ozone ppm and AQI `>= 51` class |
| `control` | shuffled ozone / AQI labels under fixed split / mode |
| `transform` | county-day NO2, CO, SO2, temperature, wind, pressure, humidity, and season -> ozone state |
| `drift` | seasonal movement, precursor loading, meteorological transport, and same-site lag movement |
| `quality` | official EPA monitor rows, observation-percent gate, physical ppm gate, county-day context coverage |
| `support` | baseline vs precursor/meteorology recovery above shuffled controls |

## Regression Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `geo_season_baseline_site_holdout` | `11` | `57,279` | `18,741` | `0.615535` | `0.377289` | `0.009384` | `0.011898` | `0.003984` |
| `precursor_meteorology_site_holdout` | `51` | `57,279` | `18,741` | `0.731717` | `0.530861` | `0.008145` | `0.011898` | `0.003984` |
| `precursor_meteorology_temporal` | `51` | `53,246` | `22,774` | `0.567709` | `0.270582` | `0.011651` | `0.014208` | `0.003984` |
| `precursor_meteorology_lag_temporal` | `56` | `52,838` | `22,442` | `0.809667` | `0.650856` | `0.008043` | `0.014125` | `0.003984` |

## AQI `>= 51` Classification Results

| Mode | Features | Train | Test | ROC AUC | AP | Balanced Acc | Macro F1 | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `geo_season_baseline_site_holdout` | `11` | `57,279` | `18,741` | `0.832772` | `0.562332` | `0.751456` | `0.667925` | `0.003984` |
| `precursor_meteorology_site_holdout` | `51` | `57,279` | `18,741` | `0.890602` | `0.641492` | `0.813394` | `0.729049` | `0.003984` |
| `precursor_meteorology_temporal` | `51` | `53,246` | `22,774` | `0.767534` | `0.578271` | `0.676272` | `0.610927` | `0.003984` |
| `precursor_meteorology_lag_temporal` | `56` | `52,838` | `22,442` | `0.872259` | `0.753047` | `0.772386` | `0.716709` | `0.003984` |

## Read

The clean read is that precursor / meteorology context strengthens the
held-out ozone-state recovery surface:

```text
geo + season baseline site-heldout:
  ozone Pearson 0.615535
  AQI AUC       0.832772

precursor + meteorology site-heldout:
  ozone Pearson 0.731717
  AQI AUC       0.890602
```

Same-site lag plus precursor / meteorology context gives the strongest
state-tracking read:

```text
ozone Pearson 0.809667
AQI AUC       0.872259
p             0.003984
```

The row seats the atmospheric branch more tightly: EPA ozone is no longer just
a single oxidant-state file; it now has official precursor and weather context
attached through the same state/control/transform/drift/quality/support stack.

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | oxygen/redox, ROS / ozone, environmental fate, and atmospheric chemistry gain precursor / meteorology context |
| `Nest 3` | atmospheric physical dynamics gain temperature, wind, pressure, and humidity context beside ozone state |
| `Nest 4` | oxygen-state biology bridge gains atmospheric precursor context before physiology rows |
| `Nest 5` | convergence routing can separate dissolved oxygen, water transport, ozone state, and precursor / meteorology context as distinct environmental-state rows |
| `FIG.14` | external adapter lane gains EPA multi-file air-monitor examples |
| `FIG.15` | support-state routing can separate baseline, precursor-context, lag-temporal, and causal-mechanism continuation gates |

## Next Gate

```text
EPA ozone precursor / meteorology seated
-> peroxide / dissolved oxidant chemistry row
-> optional smoke / PM2.5 / wildfire proxy expansion
```
