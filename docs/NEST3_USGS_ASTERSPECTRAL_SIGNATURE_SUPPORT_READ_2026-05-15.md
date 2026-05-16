# Nest 3 USGS ASTER Spectral Signature Support Read

Date: `2026-05-15`

Status: `public_safe_aggregate / real_usgs_dataset / no_raw_spectra_published`

## Architecture Description

This run is not a material-classifier side quest. It is the first clean Nest 3
physical spectral pass after the Phase 12C biology return.

The architecture being tested is the Universal Data Pattern as a measured
state-variable structure:

```text
state -> control -> transform -> drift / quality -> recurrence -> support
```

In this lane, the `state` is not a prompt label or grammar category. The state
is a real material family from the USGS Spectral Library. The `transform` is
measured reflectance resampled into ASTER spectral bands. The `control` is
shuffled material-family labels and wrong-class centroid comparisons. The
support question is whether real spectra preserve material-family separation
after that transform better than shuffled controls.

That makes the run a direct cross-pollination bridge:

```text
Phase 12C biology state variables
-> Nest 1 DE/SPEC/TOPOG formal-return language
-> Nest 3 physical spectra
-> Nest 2 material spectral signatures
-> Nest 5 convergence matrix
```

## Source

- Dataset: `USGS Spectral Library Version 7 Data`
- DOI: `10.5066/F7RR1WDJ`
- USGS data page: `https://www.usgs.gov/data/usgs-spectral-library-version-7-data`
- ScienceBase parent: `https://www.sciencebase.gov/catalog/item/5807a2a2e4b0841e59e3a18d`
- ScienceBase ASCII item: `https://www.sciencebase.gov/catalog/item/586e8c88e4b0f5ce109fccae`
- Subset used: `ASCIIdata_splib07b_rsASTER.zip`

## What Ran

The run used the ASTER-resampled ASCII subset because it is a real measured
spectral surface with a compact `9`-band vector per row.

```text
rows included after valid-band gate: 2,439
material-family classes: 7
minimum valid ASTER bands per row: 6 / 9
shuffle controls: 250
```

The public read keeps raw spectra private and reports only aggregate support
values, class counts, and separation metrics.

## State Variable Map

| Variable | This run |
| --- | --- |
| `state` | USGS chapter / material-family labels |
| `control` | shuffled material-family labels and wrong-class centroid comparisons |
| `transform` | spectra -> ASTER 9-band reflectance vectors -> centroid / derivative features |
| `drift` | deleted bands, mixtures, resampling differences, material heterogeneity |
| `artifact / quality` | minimum valid-band gate and deleted-channel handling |
| `recurrence` | many independent spectra per material family |
| `support` | spectral-angle separation and nearest-centroid classification vs shuffled controls |

## Main Result

| Metric | Real labels | Shuffled mean | Shuffled p |
| --- | ---: | ---: | ---: |
| nearest-centroid accuracy | `0.391554` | `0.072958` | `0.003984` |
| balanced accuracy | `0.517541` | `0.146808` | `0.003984` |

Read:

```text
The real material-family labels preserve spectral structure substantially above
the shuffled-label control. This is a support pass for Nest 3 Waves / Spectra
and Nest 2 Spectral Signatures.
```

## Class Summary

| Class | Rows | Median valid bands | Mean reflectance | Mean range | Within angle deg |
| --- | ---: | ---: | ---: | ---: | ---: |
| `artificial_materials` | `290` | `9.0` | `0.354904` | `0.293752` | `17.290245` |
| `coatings` | `11` | `9.0` | `0.289620` | `0.339320` | `10.485349` |
| `liquids_water_ice` | `23` | `9.0` | `0.140254` | `0.429457` | `12.667164` |
| `minerals` | `1262` | `9.0` | `0.469873` | `0.227474` | `10.918297` |
| `organic_compounds` | `360` | `6.0` | `0.352542` | `0.327835` | `12.565685` |
| `soils_mixtures` | `207` | `9.0` | `0.457480` | `0.265925` | `10.325482` |
| `vegetation` | `286` | `9.0` | `0.192121` | `0.279781` | `16.994507` |

## Separation Read

- Closest centroid pair: `minerals` vs `soils_mixtures` at `3.139515`
  degrees.
- Widest centroid pair: `coatings` vs `liquids_water_ice` at `66.875552`
  degrees.
- Maximum shuffled accuracy across `250` controls was `0.228372`, below the
  real-label accuracy of `0.391554`.
- Maximum shuffled balanced accuracy was `0.227325`, below the real-label
  balanced accuracy of `0.517541`.

## What It Supports

### Nest 3: Waves / Spectra

This run gives Nest 3 a real physical spectral dataset pass. The support is
spectral relation preservation under real material labels and shuffled-label
controls.

### Nest 2: Spectral Signatures

Because the state labels are material families, the same run becomes the
matter-facing spectral-signature row. It shows that material class structure
survives the spectral transform in a way that shuffled labels do not.

### Nest 5: Convergence

This result adds a physical spectral substrate to the convergence matrix beside
the already seated transformer, circuit / hardware-facing, structured-matter,
and biology rows.

## Boundary

This is a first ASTER-resampled spectral subset pass. It supports the
real-data spectral-signature lane. It does not close every Nest 3 waveform,
phase, terahertz, EMF, or instrument claim.

The next tightening step is one of:

1. run the native `splib07a` spectra with richer wavelength resolution;
2. run a second spectral family such as Raman / IR / THz;
3. extract the H2O / ice / liquid rows into a dedicated water lane;
4. build the Nest 5 convergence matrix from all supported rows.
