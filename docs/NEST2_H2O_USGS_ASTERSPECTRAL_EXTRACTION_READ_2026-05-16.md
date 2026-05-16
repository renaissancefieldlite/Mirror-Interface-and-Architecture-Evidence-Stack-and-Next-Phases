# Nest 2 H2O / Water Extraction From USGS ASTER Spectra

Date: `2026-05-16`

Status: `public_safe_aggregate / real_usgs_dataset / no_raw_spectra_published`

## Purpose

This is the first skeptic-proof tightening pass after the Nest 5 matrix. The
prior USGS ASTER run proved a multi-class physical spectral support surface.
This pass asks a narrower question: can the H2O / water / ice lane be extracted
as its own state family from the same real spectral source against all other
material classes and shuffled-label controls?

## State Map

| Variable | H2O extraction expression |
| --- | --- |
| `state` | USGS `liquids_water_ice` class: H2O ice, melting snow, seawater, water + montmorillonite rows |
| `control` | all non-water ASTER classes plus shuffled water-label controls |
| `transform` | ASTER-band reflectance vectors -> water-centroid spectral-angle similarity |
| `drift` | mixed snow/vegetation, seawater, water/mineral mixtures, hydrate-like false positives |
| `quality` | min valid-band gate inherited from USGS ASTER pass |
| `support` | aggregate binary water/ice extraction metrics and shuffled controls |

## Aggregate Result

- total spectra: `2,439`
- H2O / water / ice rows: `23`
- non-water controls: `2,416`
- ROC AUC: `0.918730`
- average precision: `0.121377`
- precision@23: `0.217391`
- water hits in top 23: `5 / 23`
- water hits in top 50: `8 / 23`
- water hits in top 100: `12 / 23`
- mean water angle: `0.228998` rad
- mean non-water angle: `0.720222` rad

## Shuffled Controls

- shuffle runs: `500`
- shuffled AUC mean: `0.498888`
- shuffled AUC p95: `0.597718`
- shuffled average-precision mean: `0.012146`
- shuffled precision@23 mean: `0.008522`
- p(AUC >= real): `0.001996`
- p(AP >= real): `0.001996`
- p(precision@23 >= real): `0.001996`

## Read

This pass promotes `H2O / Water` from mapped lane to first physical spectral
support row. It is not a standalone water-technology claim. It is a
support-bearing extraction: the water/ice state family separates from the rest
of the ASTER material library above shuffled-label controls using the same
state/control/transform/drift/quality/support discipline.

The important skeptic-proof value is that this is a narrower correlation
inside the broader USGS physical spectral pass. The first USGS run showed
material-family state separation. This pass asks whether one parked lane,
`H2O / Water`, can be pulled out of the same real source as its own target
state. The answer is yes at aggregate support level.

## Cross-Nest Role

- `Nest 2`: seats H2O / water as a structured-matter support row.
- `Nest 3`: strengthens Waves / Spectra by adding a narrower spectral
  extraction inside the broader USGS pass.
- `Nest 4`: creates a future hydration / metabolism / physiology bridge for
  HRV + Muse, without promoting clinical language.
- `Nest 5`: adds another independent support-state card to the convergence
  matrix.

## Boundary

Public-safe:

- aggregate metrics;
- support read;
- lane status;
- public-source dataset identity.

Private:

- source files;
- raw spectral vectors;
- scripts;
- local output tables.

## Next Gate

```text
H2O extraction seated
-> update Lattice Companion completion outline and Nest 5 matrix
-> choose next skeptic-proof gate:
   materials second target, native spectra, THz / IR / Raman, or electrochemistry
```
