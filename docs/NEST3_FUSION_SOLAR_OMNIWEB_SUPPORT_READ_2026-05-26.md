# Nest 3 Fusion + Solar OMNIWeb Support Read

Date: `2026-05-26`

Run ID: `nest3_fusion_solar_omniweb_2026-05-26`

Status: `real_data / NASA_OMNIWeb_SPDF / solar_plasma_window_gate / support; distribution/window-statistic caveat`

## Source

Primary source: `NASA OMNIWeb / SPDF OMNI2 hourly data`

Source page: `https://data.nasa.gov/dataset/omniweb-at-the-space-physics-data-facility-spdf`

Source directory: `https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/`

Format file: `omni2.text`

Local source files used: `omni2_2024.dat`, `omni2_2025.dat`

OMNI2 is described by NASA/SPDF as hourly mean interplanetary magnetic field,
solar wind plasma parameters, geomagnetic and solar activity indices, and
energetic proton fluxes measured near Earth's orbit.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | 12-hour windows with max `Kp >= 5` |
| `control` | 12-hour windows with max `Kp <= 2` |
| `step` | `6` hours |
| `group holdout` | month-level grouped cross-validation |
| `feature boundary` | geomagnetic response label columns are excluded; the model receives solar-wind, IMF, plasma, proton-flux, and solar activity features only |

## Results

| Metric | Value |
| --- | ---: |
| Source hourly rows | 17544 |
| Used windows | 1133 |
| Target / control windows | 249 / 884 |
| Feature count | 324 |
| Month groups | 24 |
| Observed ROC AUC | 0.997956 |
| Observed balanced accuracy | 0.987443 |
| Shuffled-label mean AUC | 0.500863 |
| Shuffled-label p | 0.004975 |
| Feature-shuffle AUC | 0.511353 |
| Time-order-destroyed AUC | 0.997851 |

## Interpretation

This is the first executable `Nest 3 / Fusion + Solar` source gate. It tests
whether real near-Earth solar-wind / IMF / plasma window features separate
active geomagnetic-response windows from quiet windows when the geomagnetic
label columns themselves are excluded from the feature packet.

Read as `support; distribution/window-statistic caveat`.

## Boundary

This is not a full Fusion + Solar lane closeout. It is a first OMNIWeb
solar-plasma source gate. If the time-order-destroyed control stays elevated,
the read should be described as window-statistic / solar-plasma state support
rather than raw phase-order support.

Next gate: event-block holdouts around named solar storms, solar-cycle
seasonal/null controls, and an adjacent NASA POWER solar-radiation comparator.
