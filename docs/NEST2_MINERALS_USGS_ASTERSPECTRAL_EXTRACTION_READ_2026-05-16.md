# Nest 2 Minerals Extraction From USGS ASTER Spectra

Date: `2026-05-16`

Status: `public_safe_aggregate / real_usgs_dataset / no_raw_spectra_published`

## Purpose

This is the next skeptic-proof tightening pass after the H2O / water
extraction. The prior USGS ASTER run proved a multi-class physical
spectral support surface. This pass asks whether the mineral family can
be recovered as a broad structured-matter state against all non-mineral
material classes and shuffled-label controls.

## State Map

| Variable | Minerals extraction expression |
| --- | --- |
| `state` | USGS `minerals` class across ASTER reflectance bands |
| `control` | artificial materials, coatings, liquids/water/ice, organic compounds, soils/mixtures, vegetation, plus shuffled mineral-label controls |
| `transform` | ASTER-band reflectance vectors -> binary centroid margin: non-mineral angle minus mineral angle |
| `drift` | soils/mineral mixtures, vegetation/mineral adjacency, broad mineral-family heterogeneity |
| `quality` | min valid-band gate inherited from USGS ASTER pass |
| `support` | aggregate binary mineral extraction metrics and shuffled controls |

## Aggregate Result

- total spectra: `2,439`
- mineral rows: `1,262`
- non-mineral controls: `1,177`
- ROC AUC: `0.714217`
- average precision: `0.735238`
- precision@1262: `0.657686`
- mineral hits in top 1262: `830 / 1262`
- mineral hits in top 100: `92 / 1262`
- mineral hits in top 250: `221 / 1262`
- mean mineral angle to mineral centroid: `0.190560` rad
- mean non-mineral angle to mineral centroid: `0.324346` rad

## Shuffled Controls

- shuffle runs: `500`
- shuffled AUC mean: `0.515552`
- shuffled AUC p95: `0.529232`
- shuffled average-precision mean: `0.531157`
- shuffled precision@1262 mean: `0.528106`
- p(AUC >= real): `0.001996`
- p(AP >= real): `0.001996`
- p(precision@1262 >= real): `0.001996`

## Read

This pass promotes `Minerals` from a partially supported / mapped lane
to a direct physical spectral support row. The claim level is support-bearing
extraction: the mineral state family separates from non-mineral ASTER material
families above shuffled-label controls using the same
state/control/transform/drift/quality/support discipline.

## Cross-Nest Role

- `Nest 2`: seats minerals as a structured-matter support row.
- `Nest 3`: strengthens Waves / Spectra by adding a second narrowed extraction inside the USGS pass.
- `Nest 5`: adds another independent support-state card to the convergence matrix.

## Boundary

Public-safe: aggregate metrics, support read, and lane status.

Private: source files, raw spectral vectors, scripts, and local output tables.

## Next Gate

```text
Minerals extraction seated
-> update Lattice Companion completion outline and Nest 5 matrix
-> choose next skeptic-proof gate:
   materials second target, electrochemistry, catalysis / conditions, or native IR/Raman/THz spectra
```
