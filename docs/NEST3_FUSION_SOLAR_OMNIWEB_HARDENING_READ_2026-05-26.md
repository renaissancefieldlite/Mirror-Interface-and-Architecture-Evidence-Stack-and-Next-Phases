# Nest 3 Fusion + Solar OMNIWeb Hardening Read

Date: `2026-05-26`

Run ID: `nest3_fusion_solar_omniweb_hardening_2026-05-26`

Status: `real_data / NASA_OMNIWeb_SPDF / solar_plasma_hardening_gate / hardened support; window-statistic caveat`

## Source

Primary source: `NASA OMNIWeb / SPDF OMNI2 hourly data`

Source page: `https://data.nasa.gov/dataset/omniweb-at-the-space-physics-data-facility-spdf`

Source directory: `https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/`

Local source files used: `omni2_2024.dat`, `omni2_2025.dat`

## State / Control

| Role | Definition |
| --- | --- |
| `target` | 12-hour windows with max `Kp >= 5` |
| `control` | 12-hour windows with max `Kp <= 2` |
| `event-block holdout` | active windows grouped into storm/event blocks using <= `36` hour gaps; quiet controls grouped by quiet dates |
| `seasonal/null controls` | same-active-month subset, within-month label shuffle, and calendar-only model |
| `feature boundary` | geomagnetic response labels remain excluded; model receives solar-wind, IMF, plasma, proton-flux, and solar-activity features |

## Results

| Metric | Value |
| --- | ---: |
| Source hourly rows | 17544 |
| Used windows | 1133 |
| Target / control windows | 249 / 884 |
| Event blocks | 57 |
| Feature count | 324 |
| Event-block AUC | 0.998851 |
| Event-block balanced accuracy | 0.990582 |
| Event-block shuffled-label mean AUC | 0.500907 |
| Event-block shuffled-label p | 0.004975 |
| Event-block within-month shuffle AUC | 0.574688 |
| Event-block feature-shuffle AUC | 0.501022 |
| Same-active-month AUC | 0.998667 |
| Same-active-month balanced accuracy | 0.990561 |
| Same-active-month shuffled-label p | 0.004975 |
| Same-active-month within-month shuffle AUC | 0.545004 |
| Same-active-month feature-shuffle AUC | 0.502326 |
| Calendar/season-only AUC | 0.630742 |
| Calendar/season-only balanced accuracy | 0.617890 |

## High-Activity Event Blocks

| Event block | Start UTC | End UTC | Windows | Max Kp |
| --- | --- | --- | ---: | ---: |
| `storm_block_08_20240510_20240513` | 2024-05-10T06:00:00 | 2024-05-13T00:00:00 | 11 | 90.0 |
| `storm_block_55_20251111_20251113` | 2025-11-11T18:00:00 | 2025-11-13T06:00:00 | 7 | 87.0 |
| `storm_block_22_20241010_20241011` | 2024-10-10T06:00:00 | 2024-10-11T12:00:00 | 6 | 87.0 |
| `storm_block_02_20240323_20240325` | 2024-03-23T12:00:00 | 2024-03-25T00:00:00 | 6 | 83.0 |
| `storm_block_26_20241231_20250101` | 2024-12-31T18:00:00 | 2025-01-01T18:00:00 | 5 | 80.0 |
| `storm_block_41_20250531_20250604` | 2025-05-31T18:00:00 | 2025-06-04T12:00:00 | 14 | 77.0 |
| `storm_block_36_20250415_20250416` | 2025-04-15T06:00:00 | 2025-04-16T18:00:00 | 7 | 77.0 |
| `storm_block_11_20240628_20240628` | 2024-06-28T00:00:00 | 2024-06-28T12:00:00 | 3 | 77.0 |

## Interpretation

This hardens the first `Nest 3 / Fusion + Solar` OMNIWeb source gate by testing
whether solar-wind / IMF / plasma features still separate active and quiet
windows when whole storm/event blocks are held out and seasonal/null controls
are applied.

Read as `hardened support; window-statistic caveat`.

## Boundary

This strengthens the first-pass Fusion + Solar read, but it remains a
solar-plasma window-statistic support row. It is not raw phase-order proof and
not a full solar-cycle closeout.

Next gate: adjacent NASA POWER solar-radiation comparator or a longer
solar-cycle OMNIWeb span with event-family holdouts.
