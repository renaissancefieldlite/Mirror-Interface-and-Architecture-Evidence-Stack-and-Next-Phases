# Nest 3 Gravity / Orbits Exoplanet Support Read

Date: `2026-05-26`

Run ID: `nest3_gravity_orbits_exoplanet_resonance_2026-05-26`

Status: `real_data / NASA_Exoplanet_Archive / adjacent_orbit_pair_gate / support; first-pass orbit-architecture caveat`

## Source

Primary source: `NASA Exoplanet Archive Planetary Systems Composite Parameters (pscomppars)`

Source page: `https://exoplanetarchive.ipac.caltech.edu/`

TAP query endpoint: `https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,sy_pnum,pl_orbper,pl_orbsmax,pl_orbeccen,pl_orbincl,pl_rade,pl_bmasse,st_mass,st_rad+from+pscomppars+where+pl_orbper+is+not+null+and+hostname+is+not+null&format=csv`

Local source file used: `nasa_exoplanet_pscomppars_orbits.csv`

The source rows are confirmed exoplanet orbital and host-star parameters from
the NASA Exoplanet Archive composite planetary-systems table.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | adjacent planet pairs within `3%` of low-order period ratios `5:4, 4:3, 3:2, 5:3, 2:1, 3:1` |
| `control` | adjacent planet pairs at least `12%` away from the same low-order period ratios |
| `group holdout` | host-system-held-out GroupKFold |
| `feature boundary` | nearest-resonance label, direct resonance distance, state label, host name, and planet names excluded |

## Results

| Metric | Value |
| --- | ---: |
| Source planet rows | 5951 |
| Source systems | 4382 |
| Multi-planet systems | 1049 |
| Used adjacent pairs | 836 |
| Target / control pairs | 378 / 458 |
| Host-system groups | 637 |
| Feature count | 60 |
| Observed ROC AUC | 0.943642 |
| Observed balanced accuracy | 0.859754 |
| Shuffled-label mean AUC | 0.498468 |
| Shuffled-label p | 0.004975 |
| Feature-shuffle AUC | 0.464407 |
| Geometry-only AUC | 0.961917 |
| No-orbit-geometry AUC | 0.729053 |

## Interpretation

This is the first executable `Nest 3 / Gravity / Orbits` source gate. It tests
whether real adjacent-planet orbital architecture separates near low-order
period-resonance pairs from far off-resonance adjacent pairs under
host-system-held-out validation.

Read as `support; first-pass orbit-architecture caveat`.

## Boundary

This is not a full dynamical resonance proof, and it is not an ephemeris
integration. The state is based on observed adjacent period ratios from a public
confirmed-exoplanet orbital-parameter table. The direct resonance-distance label
is excluded, but pair geometry remains the expected signal carrier.

Next gate: harder orbit controls using public ephemeris or orbital-element rows,
including random-pair nulls, resonance-family holdouts, and time/epoch-aware
orbit propagation if a clean ephemeris source is selected.
