# Nest 3 Raman Spectral-Family UDP Support Read

Date: `2026-05-24`

Run ID: `nest3_ramdb_raman_udp_2026-05-24`

Status: `real_data / NASA_Ames_Ramdb / second_spectral_family_candidate_support`

## Source

Dataset surface: NASA Ames Ramdb Raman Spectroscopic Database.

Ramdb page: https://www.astrochemistry.org/ramdb/

Ramdb paper DOI: https://doi.org/10.1016/j.icarus.2023.115769

This pass uses public Raman detail pages and their published transition tables.
It does not yet use the full raw downloadable CSV bundle.

## Universal Data Pattern Packet

| Field | Value |
| --- | --- |
| `source` | NASA Ames Ramdb Raman transition tables |
| `state` | amino-acid Raman records |
| `control` | mineral-standard Raman records |
| `transform` | Raman-shift binned peak area / height / count features plus peak summary features |
| `score` | grouped cross-validated ROC AUC / AP / balanced accuracy |
| `controls` | group-shuffled labels, feature shuffle, band-position shuffle |
| `group holdout` | compound-level grouping where possible |

## Data Shape

| Measure | Value |
| --- | ---: |
| total Raman records | 66 |
| amino-acid records | 24 |
| mineral records | 42 |
| feature count | 205 |
| target compounds | 8 |
| control compounds | 10 |

## Scores

| Metric | Observed | Group-shuffled labels | Feature shuffle | Band-position shuffle |
| --- | ---: | ---: | ---: | ---: |
| ROC AUC | 0.996296 | 0.497985 | 0.537037 | 0.918519 |
| Average precision | 0.995238 | -- | 0.444052 | 0.810833 |
| Balanced accuracy | 0.927778 | -- | 0.488889 | 0.794444 |

Feature-family checks:

| Feature family | ROC AUC | Average precision | Balanced accuracy |
| --- | ---: | ---: | ---: |
| binned peak features only | 0.994444 | 0.995238 | 0.938889 |
| non-binned summary features only | 1.000000 | 1.000000 | 0.988889 |
| all features except laser wavelength | 1.000000 | 1.000000 | 0.950000 |

Permutation p-value against group-shuffled labels:

```text
0.003984
```

Folds:

```text
5
```

Permutation repeats:

```text
250
```

## Support Read

The observed Raman transition feature packet separates amino-acid records from
mineral-standard records above the group-shuffled label control and the
feature-shuffle control. This is a candidate support row for the `Nest 3 /
Waves-Spectra / second physical spectral family` lane.

The band-position shuffle remained elevated instead of fully collapsing, so the
clean read is class-level Raman transition-structure support. It is not yet a
pure phase-lock / spectral-position closeout.

The clean interpretation is:

```text
public Raman source -> state/control spectral family -> peak/band transform
-> group and band controls -> support read
```

## Boundary

This is not a full Ramdb raw-spectrum closeout, not a Terahertz closeout, and
not a closure of all Nest 3. It is the first executable second-spectral-family
support row. The full Nest 3 lane list remains open: Terahertz, Fire + Plasma,
Fusion + Solar, Space / Time / Cycles, Gases / Liquids / Phases, Gravity /
Orbits, EMF / Fields, Oscillators / Resonance, and Waves / Spectra /
Phase-Lock.

## Next Gates

1. Pull or request the full Ramdb raw / processed CSV bundle and rerun on
   continuous spectra rather than peak tables only.
2. Run PAH versus amino-acid or carbon-allotrope versus mineral controls.
3. Source the Fire + Plasma lane.
4. Source EMF / Fields and Oscillators / Resonance as paired dynamics lanes.
