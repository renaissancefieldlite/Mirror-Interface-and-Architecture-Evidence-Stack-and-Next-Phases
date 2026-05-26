# Nest 3 Fusion + Solar Source Gate Plan

Date: `2026-05-26`

Status: `source_gate_executed / public_support_read_available`

## Lane

`Nest 3 / Fusion + Solar`

This lane extends the Fire + Plasma, EMF / Fields, and Oscillators /
Resonance rows into solar-plasma dynamics. The first executable gate should
use public heliophysics rows with explicit active / quiet windows and controls
that break label, feature, timing, and seasonal structure.

## Primary Source

Primary source: `NASA OMNIWeb / SPDF`

Source page: `https://data.nasa.gov/dataset/omniweb-at-the-space-physics-data-facility-spdf`

Planned rows:

- near-Earth solar wind magnetic-field measurements
- solar wind speed / density / plasma-temperature rows where available
- geomagnetic response rows as adjacent context only, not as the first target
  label unless the source manifest makes that label explicit

## Backup / Adjacent Source

Backup / adjacent source: `NASA POWER Hourly API`

API docs: `https://power.larc.nasa.gov/docs/services/api/temporal/hourly/`

Use only as adjacent solar-radiation / meteorological time-series support if
OMNIWeb access is unavailable or if the first gate needs an earth-surface
solar-energy comparator. POWER rows do not replace heliophysics plasma rows.

## Planned State / Control

| Role | Planned definition |
| --- | --- |
| `target` | active solar / plasma disturbance windows, selected from source-field behavior and explicit activity thresholds |
| `control` | quiet solar-wind / plasma windows sampled away from active disturbance windows |
| `holdout` | year or month blocks, or storm/event blocks if event labels are used |
| `null` | seasonal / local-time / calendar-only controls |

## Planned Controls

- shuffled-label control
- feature-shuffle control
- time-order-destroyed control
- seasonal / calendar null
- event-block or month-block holdout
- adjacent context check to ensure the read is not merely calendar, diurnal, or
  source-format leakage

## Public-Safe Output

Expected artifacts after execution:

```text
experiments/nest3_fusion_solar_omniweb/run_omniweb_solar_plasma_gate.py
experiments/nest3_fusion_solar_omniweb/results/nest3_fusion_solar_omniweb_2026-05-26.json
docs/NEST3_FUSION_SOLAR_OMNIWEB_SUPPORT_READ_2026-05-26.md
```

Raw downloaded payloads stay out of the public repo unless later cleared by
license, size, and public/private review. Public docs should cite the source,
date range, source manifest, row count, label definition, controls, scores,
and boundary.

## Executed Support Read

The first source gate was executed on `2026-05-26`:

```text
docs/NEST3_FUSION_SOLAR_OMNIWEB_SUPPORT_READ_2026-05-26.md
```

The result is `support; distribution/window-statistic caveat`.

## Boundary

This plan created the source gate and now points to the first support read.
The lane is not fully closed; named storm/event blocks, solar-cycle nulls, and
NASA POWER adjacency remain next gates.
