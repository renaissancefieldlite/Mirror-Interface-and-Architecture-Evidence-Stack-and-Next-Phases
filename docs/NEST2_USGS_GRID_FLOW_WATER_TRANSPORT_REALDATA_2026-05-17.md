# Nest 2 / Nest 3 USGS Grid-Flow Water-Transport Real-Data Row

Status: `public_safe_support_read / local_not_yet_pushed`

## Front-Center Read

The H2O / water, environmental-fate, and physical-flow branches now have a
seated grid-flow / water-transport real-data row.

This pass uses USGS instantaneous hydrology sensor data and tests whether
same-site same-hour gage height, site calibration, timing, and stage movement
recover discharge state and site-relative high-flow class above shuffled
controls.

The row matters because the water branch now has both chemistry-state support
and transport-state support:

```text
USGS dissolved oxygen -> oxygen/redox water-quality state
USGS grid-flow -> discharge/stage water-transport state
```

## Source

- Source: USGS NWIS instantaneous values
- API: <https://waterservices.usgs.gov/nwis/iv/>
- Query: Colorado, 7-day window, active sites, parameter codes `00060`, `00065`
- `00060`: discharge, cubic feet per second
- `00065`: gage height, feet

## Target QA

- time series: `714`
- raw long rows: `608,405`
- raw discharge rows: `296,515`
- raw gage-height rows: `311,890`
- complete raw rows: `288,392`
- complete raw sites: `328`
- hourly support rows: `54,825`
- hourly support sites: `328`
- discharge range: `0.000` to `4,165.000` cfs
- discharge mean / median: `177.837` / `31.425` cfs
- gage-height range: `-0.235` to `18.270` ft
- high-flow definition: `site-relative discharge >= site q75`
- high-flow rows: `16,034`
- shuffled controls per read: `250`

Invalid sensor sentinels and impossible values are removed before modeling.

## State Map

| Variable | Grid-flow expression |
| --- | --- |
| `state` | discharge cfs, log discharge, and site-relative high-flow class |
| `control` | shuffled flow labels under fixed split / mode |
| `transform` | gage height, site-stage calibration, timing, site geometry -> flow state |
| `drift` | stage movement, diurnal / storm timing, site-relative high-flow movement |
| `quality` | same-site same-hour rows, physical value gates, minimum 24-hour site support |
| `support` | site-heldout and same-site temporal recovery above shuffled controls |

## Regression Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `stage_site_holdout` | `7` | `41,235` | `13,590` | `0.511057` | `0.241737` | `1.983033` | `2.321929` | `0.003984` |
| `stage_calibrated_site_holdout` | `12` | `41,090` | `13,735` | `0.666581` | `0.415335` | `1.609808` | `2.105628` | `0.003984` |
| `stage_calibrated_temporal` | `13` | `38,228` | `16,597` | `0.998131` | `0.995992` | `0.136331` | `2.158668` | `0.003984` |

## High-Flow Classification Results

| Mode | Features | Train | Test | ROC AUC | AP | Balanced Acc | Macro F1 | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `stage_site_holdout` | `7` | `41,205` | `13,620` | `0.711309` | `0.484670` | `0.620812` | `0.627606` | `0.003984` |
| `stage_calibrated_site_holdout` | `12` | `41,010` | `13,815` | `0.978827` | `0.951340` | `0.902925` | `0.912663` | `0.003984` |
| `stage_calibrated_temporal` | `13` | `38,228` | `16,597` | `0.991244` | `0.983492` | `0.956645` | `0.952289` | `0.003984` |

## Read

USGS grid-flow seats water transport as a real sensor-state surface with two
separate support modes:

- site-heldout generalization: gage-height and timing features recover flow
  state across held-out sites with Pearson `0.511057` before site calibration
  and Pearson `0.666581` after site-stage calibration
- same-site temporal tracking: stage-calibrated temporal mode recovers log
  discharge with Pearson `0.998131`, R2 `0.995992`, and high-flow ROC AUC
  `0.991244`

The clean public claim is that water transport now has a real stage-to-discharge
support surface with explicit shuffled-label controls. Site-heldout
generalization and same-site calibrated temporal tracking should remain
separate in claim-support language because they answer different validation
questions.

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | H2O / water, environmental fate, electrochemistry-adjacent sensor state, and transport rows gain real hydrology support |
| `Nest 3` | physical sensor / flow-state dynamics row gains discharge-stage temporal and site-heldout support |
| `Nest 4` | oxygen-state biology bridge now has an environmental transport precursor beside dissolved oxygen |
| `Nest 5` | convergence matrix can route water chemistry, flow transport, site calibration, and environmental-state tracking as one support family |
| `FIG.14` | external adapter lane includes hydrology / water-transport sensor examples |
| `FIG.15` | support-state routing can separate site-heldout generalization, calibrated temporal tracking, and ROS / broader basin continuation gates |

## Next Gate

```text
USGS grid-flow seated
-> ROS / ozone / peroxide real-data row
-> optional broader basin / precipitation / flow-routing expansion
```
