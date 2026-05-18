# Nest 2 / Nest 3 EPA Ozone Oxidant-State Real-Data Row

Status: `public_safe_support_read / local_not_yet_pushed`

## Front-Center Read

The oxygen / redox, ROS / ozone, environmental-state, and physical-atmosphere
branches now have a seated ozone oxidant-state real-data row.

This pass uses official EPA AirData daily ozone monitor records and tests
whether geography, season, monitor QA, regional context, and prior same-site
state recover daily ozone maximum and AQI `>= 51` class above shuffled controls.

The row matters because the water/oxygen branch now has three complementary
real public surfaces:

```text
USGS dissolved oxygen -> water chemistry / oxygen state
USGS grid-flow -> water transport / discharge-stage state
EPA ozone -> atmospheric oxidant / reactive-oxygen state
```

## Source

- Source: EPA AirData daily ozone
- Public file: <https://aqs.epa.gov/aqsweb/airdata/daily_44201_2025.zip>
- Parameter code: `44201`
- Pollutant standard: `Ozone 8-hour 2015`
- Units: parts per million

## Target QA

- clean rows: `243,461`
- monitor sites: `1,205`
- states / territories: `53`
- date range: `2025-01-01` to `2025-10-30`
- ozone maximum range: `0.000000` to `0.142000` ppm
- ozone mean / median: `0.042986` / `0.043000` ppm
- high-ozone class: `AQI >= 51`
- high-ozone rows: `36,028`
- shuffled controls per read: `250`

Rows are gated to the `Ozone 8-hour 2015` standard with observation-percent
and physical ppm checks before modeling.

## State Map

| Variable | EPA ozone expression |
| --- | --- |
| `state` | daily 8-hour ozone maximum ppm and AQI `>= 51` class |
| `control` | shuffled ozone / AQI labels under fixed split / mode |
| `transform` | geography, season, monitor QA, regional context, site timing -> ozone state |
| `drift` | seasonal movement, regional ozone loading, same-site lag / recovery movement |
| `quality` | official EPA monitor rows, observation-percent gate, physical ppm gate |
| `support` | site-heldout and same-site temporal recovery above shuffled controls |

## Regression Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `geo_season_site_holdout` | `10` | `182,940` | `60,521` | `0.432201` | `0.186133` | `0.009746` | `0.010804` | `0.003984` |
| `regional_site_holdout` | `11` | `182,940` | `60,521` | `0.438556` | `0.189183` | `0.009728` | `0.010804` | `0.003984` |
| `site_lag_temporal` | `16` | `169,033` | `72,018` | `0.743096` | `0.505350` | `0.008552` | `0.012170` | `0.003984` |

## AQI `>= 51` Classification Results

| Mode | Features | Train | Test | ROC AUC | AP | Balanced Acc | Macro F1 | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `geo_season_site_holdout` | `10` | `182,940` | `60,521` | `0.761993` | `0.372342` | `0.690354` | `0.593171` | `0.003984` |
| `regional_site_holdout` | `11` | `182,940` | `60,521` | `0.760048` | `0.394923` | `0.686715` | `0.599442` | `0.003984` |
| `site_lag_temporal` | `16` | `169,033` | `72,018` | `0.879495` | `0.625808` | `0.795352` | `0.686737` | `0.003984` |

## Read

EPA ozone seats atmospheric oxidant state as a real public monitoring surface.

The support modes should be kept distinct:

- site-heldout modes show that geography, season, monitor QA, and regional
  context recover ozone state across held-out monitors above shuffled labels
- same-site temporal mode shows stronger day-to-day oxidant-state tracking
  when prior monitor state is available

The clean public claim is that the ROS / ozone branch now has a real oxidant
state row with explicit shuffled-label controls. Peroxide and dissolved oxidant
chemistry remain continuation gates for solution-phase reactive-oxygen support.

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | oxygen/redox, ROS / ozone, environmental fate, and atmospheric chemistry rows gain real ozone support |
| `Nest 3` | physical atmosphere / sensor-state dynamics row gains site-heldout and same-site temporal oxidant-state support |
| `Nest 4` | oxygen-state biology bridge now has atmospheric oxidant context beside dissolved oxygen and water transport |
| `Nest 5` | convergence matrix can route water oxygen, water transport, and atmospheric oxidant state as one oxygen / environment support family |
| `FIG.14` | external adapter lane includes ozone / atmospheric sensor examples |
| `FIG.15` | support-state routing can separate site-heldout generalization, temporal tracking, and peroxide / precursor continuation gates |

## Next Gate

```text
EPA ozone seated
-> peroxide / dissolved oxidant chemistry row
-> optional meteorology / wildfire-smoke / precursor expansion
```
