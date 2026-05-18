# Nest 2 / Nest 3 EIS Peak And Band-Family Diagnostics

Status: `public_safe_support_read / local_not_yet_pushed`

## Front-Center Read

The EIS branch now has an explainable peak / band-family support read.

The earlier frequency-resolved EIS pass showed that continuous SOH tracking
works when EIS is paired with cycle context or per-battery baseline-delta
calibration. This follow-up compresses the ordered complex EIS sweep into
low / mid / high band summaries, peak movement, prominence, centroid, spread,
and baseline-delta band features.

## Source

- NASA PCoE Battery Data Set: <https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/>

## Target QA

- clean linked EIS rows: `1,477`
- batteries: `34`
- ordered sweep bins per vector: `24`
- band feature count: `828`
- shuffled controls per read: `250`

Band families are ordered-sweep bins, not explicit Hz values, because the NASA
MAT impedance records expose ordered complex vectors without a parsed frequency
vector.

## State Map

| Variable | Peak / band-family EIS expression |
| --- | --- |
| `state` | low / mid / high EIS band shape, peak location, peak prominence, centroid, linked SOH |
| `control` | shuffled SOH labels under fixed split / mode |
| `transform` | complex EIS vectors -> ordered bands, peak metrics, baseline deltas |
| `drift` | cycle aging, band movement, peak migration, capacity fade |
| `quality` | same target QA as frequency-resolved SOH run |
| `support` | group-holdout and temporal regression above shuffled controls |

## Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `band_group_holdout` | `279` | `783` | `694` | `0.148524` | `-0.285542` | `0.149576` | `0.139873` | `0.003984` |
| `band_cycle_group_holdout` | `281` | `1,036` | `441` | `0.843785` | `0.514831` | `0.066512` | `0.096093` | `0.003984` |
| `delta_band_group_holdout` | `831` | `1,321` | `156` | `0.807991` | `0.593023` | `0.083207` | `0.144752` | `0.003984` |
| `delta_band_cycle_group_holdout` | `833` | `1,267` | `210` | `0.787890` | `0.568246` | `0.115243` | `0.205008` | `0.003984` |
| `delta_band_same_battery_temporal` | `555` | `1,011` | `454` | `0.942284` | `0.782651` | `0.071334` | `0.188363` | `0.003984` |
| `delta_band_cycle_same_battery_temporal` | `833` | `1,011` | `454` | `0.956571` | `0.850803` | `0.059101` | `0.188363` | `0.003984` |

## Top Feature Families

| Rank | Variant | Vector | Component | Importance |
| ---: | --- | --- | --- | ---: |
| 1 | `delta` | `rectified_impedance` | `real` | `0.100436` |
| 2 | `delta` | `rectified_impedance` | `abs` | `0.088759` |
| 3 | `delta` | `rectified_impedance` | `imag` | `0.078769` |
| 4 | `delta` | `current_ratio` | `abs` | `0.062613` |
| 5 | `raw` | `rectified_impedance` | `abs` | `0.061436` |
| 6 | `delta` | `current_ratio` | `real` | `0.060891` |

## Read

Peak / band-family diagnostics make the EIS support more readable. Ordered
shape summaries, peak movement, and baseline-delta band changes carry SOH most
clearly when seated in a cycle or same-battery temporal frame.

Clean support language:

```text
EIS peak / band-family diagnostics support continuous SOH tracking through
ordered impedance-shape movement, especially delta rectified-impedance and
current-ratio band features. Same-battery temporal delta-band + cycle context
is the strongest current support mode.
```

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | electrochemistry / battery-health row gains interpretable impedance-shape support |
| `Nest 3` | waveform / spectra / impedance branch gains peak and band-family diagnostics |
| `Nest 5` | convergence matrix can carry boundary, support, calibration, and temporal-tracking modes separately |
| `FIG.14` | external adapter lane includes EIS shape diagnostics |
| `FIG.15` | support-state routing can distinguish raw band, cycle-context, delta-band, and temporal support |

## Next Gate

```text
peak / band-family diagnostics seated
-> conductivity real-data row
-> dissolved oxygen / ROS or grid-flow continuation row
```
