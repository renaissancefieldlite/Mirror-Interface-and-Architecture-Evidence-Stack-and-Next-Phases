# Nest 2 Frequency-Resolved EIS-to-SOH Follow-Up

Status: `public_safe_support_read / local_not_yet_pushed`

## Front-Center Read

The continuous EIS-to-SOH branch now has a stronger frequency-resolved read.

The earlier EIS result correctly separated degraded-state classification from
continuous SOH regression. This follow-up adds target QA, frequency-bin
features from the complex EIS vectors, calibrated baseline deltas, and
same-battery temporal tracking. The result is a cleaner support surface instead
of one flattened EIS number.

## Source

- NASA PCoE Battery Data Set: <https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/>

## Target QA

- raw discharge rows: `2,794`
- valid positive discharge rows: `2,542`
- raw impedance rows: `1,956`
- clean linked impedance rows: `1,477`
- batteries: `34`
- frequency bins per vector: `24`
- base frequency feature count: `290`
- shuffled controls per read: `250`

Target QA removes zero / invalid capacity rows before linking impedance cycles
to nearest discharge capacity. SOH is computed as capacity divided by the first
valid positive capacity for the same battery.

## State Map

| Variable | Frequency-resolved EIS expression |
| --- | --- |
| `state` | complex impedance vectors, resistance terms, linked SOH |
| `control` | shuffled SOH labels under fixed split / mode |
| `transform` | complex EIS vectors -> real / imag / abs / phase bins, baseline deltas, temporal tracking |
| `drift` | cycle aging, frequency-bin movement, Re / Rct movement, capacity fade |
| `quality` | zero / invalid capacity rows removed; nearest discharge link constrained |
| `support` | group-holdout and same-battery temporal regression above shuffled controls |

## Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `freq_bins_group_holdout` | `291` | `783` | `694` | `0.041700` | `-0.487115` | `0.160876` | `0.139873` | `0.254980` |
| `freq_bins_plus_cycle_group_holdout` | `293` | `1,036` | `441` | `0.845177` | `0.540143` | `0.064753` | `0.096093` | `0.003984` |
| `delta_freq_cycle_group_holdout` | `873` | `1,321` | `156` | `0.855461` | `0.685404` | `0.073157` | `0.144752` | `0.003984` |
| `delta_freq_no_cycle_same_battery_temporal` | `581` | `1,011` | `454` | `0.947804` | `0.795559` | `0.069183` | `0.188363` | `0.003984` |
| `delta_freq_cycle_same_battery_temporal` | `873` | `1,011` | `454` | `0.954291` | `0.856414` | `0.057979` | `0.188363` | `0.003984` |

## Read

Frequency-resolved EIS separates the earlier continuous-SOH boundary into four
usable pieces:

- pure frequency bins without cycle context do not generalize across held-out
  batteries
- frequency bins plus cycle context recover SOH above shuffled controls
- calibrated frequency-delta features strengthen the group-holdout read
- same-battery temporal frequency deltas give the strongest continuous SOH
  tracking surface

The clean support language is:

```text
Frequency-resolved EIS supports continuous SOH tracking when paired with cycle
context or per-battery baseline-delta calibration. Pure uncalibrated
cross-battery EIS remains an open continuation gate.
```

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | electrochemistry / battery-health lane gains frequency-resolved SOH support |
| `Nest 3` | impedance waveform branch now includes binned complex EIS movement, not only scalar Re / Rct |
| `Nest 5` | convergence matrix can separate uncalibrated boundary, cycle-context support, and temporal tracking support |
| `FIG.14` | external adapter examples include frequency-resolved EIS |
| `FIG.15` | support-state routing can track boundary / support / calibration mode separately |

## Next Gate

```text
frequency-resolved EIS-to-SOH seated
-> peak / band-family diagnostics
-> dissolved oxygen / ROS or membrane / conductivity / grid-flow row
```
