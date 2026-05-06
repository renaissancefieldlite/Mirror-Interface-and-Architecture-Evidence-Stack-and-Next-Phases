# Nest 4A HRV Biological Comparator Gate

Date: `2026-05-05`

Status: `control_supported_condition_separation / coarse_biology_adapter_supported`

## Purpose

This gate advances the next executable layer after parking `ARC15`. `ARC15 /
FG200.67` remains an operator-run physical bench lane. The available measured
surface for the next layer is the completed `Phase 12B` HRV comparator matrix:

```text
5 runs x 4 conditions = 20 live physiology sessions
```

This is a `Nest 4` biological comparator pass. It tests whether live HRV
condition classes preserve separable state structure under the same
target/control/shuffle discipline used across the architecture stack.

## Input Surface

Source artifact:

```text
artifacts/v8/phase12b_biological_comparison_pack/
  v8_phase12b_biological_comparison_pack_data_2026-04-24.json
```

Condition classes:

| Condition | Runs |
| --- | ---: |
| `seated_calm` | `5` |
| `drift_control` | `5` |
| `mirror_coherence` | `5` |
| `dancing_activation` | `5` |

Scored feature sets:

| Feature set | Fields |
| --- | --- |
| `HR-only` | `delta_hr` |
| `multi-feature HRV` | `delta_hr`, `delta_rmssd`, `delta_sdnn`, `post_minus_condition_hr`, `post_minus_condition_rmssd`, `post_minus_condition_sdnn` |

Controls:

- balanced label shuffle preserving `5` sessions per condition
- within-run block shuffle preserving one label per condition block
- leave-one-run-index-out nearest-centroid classification

## Run Result

The rerun wrote:

```text
artifacts/validation/phase12b_biological_control_closeout/
```

Main result:

```text
status = control_supported_condition_separation
```

Condition means:

| Condition | Mean delta HR |
| --- | ---: |
| `seated_calm` | `-1.651248` |
| `drift_control` | `5.333063` |
| `mirror_coherence` | `-7.943775` |
| `dancing_activation` | `6.517002` |

Control table:

| Test | Observed | Null mean | p-value |
| --- | ---: | ---: | ---: |
| HR-only leave-one-run-out accuracy | `0.5` | `0.243962` | `0.022649` |
| HR-only leave-one-run-out accuracy, within-run block shuffle | `0.5` | `0.249893` | `0.033148` |
| Multi-feature leave-one-run-out accuracy | `0.45` | `0.229268` | `0.047598` |
| Multi-feature leave-one-run-out accuracy, within-run block shuffle | `0.45` | `0.249632` | `0.072346` |
| Mirror delta HR lower than shuffled labels | `-7.943775` | `0.561673` | `0.002` |
| Dancing-minus-mirror delta HR gap | `14.460777` | `-0.005609` | `0.0012` |
| Mirror-vs-calm multi-feature distance | `56.837712` | `31.67036` | `0.041248` |

## Read

`mirror_coherence` is the strongest HR-downshift state in the completed
matrix, while `dancing_activation` is the activation state. The
`dancing_activation - mirror_coherence` delta-HR gap clears shuffled-label
controls, and HR-only leave-one-run-out classification clears both balanced and
within-run block shuffles.

The multi-feature HRV readout is supportive on balanced shuffle and softer on
within-run block shuffle. That gives the lane a clean current shape:

```text
HRV supports coarse biological state separation.
Delta HR is the strongest current biology signal.
Multi-feature HRV becomes stronger with the planned larger matrix.
```

## Meaning For The Ladder

This is the first active `Nest 4` biological comparator after the `Nest 3`
timing/coherence pass:

```text
Nest 3D / 3L hardware timing-coherence
-> Nest 4A HRV biological state separation
-> later EEG + HRV timing / spectral / topographic biology
-> return into nutrition, metabolism, biomolecular primitives, and
   structured-matter safety rows
```

`ARC15` stays parked as a physical operator-run branch. `Nest 4A` moves forward
because the HRV sessions already exist as live measured rows.

## Next Gate

The next biology expansion is `Phase 12B-L20`:

```text
20 blocks x 4 conditions = 80 sessions
Latin-square condition order
same condition vocabulary
raw RR export whenever available
```

The longer-range `Nest 4` upgrade is simultaneous `EEG + HRV`, which supplies
alpha/theta/band-power/phase-lock and topographic features beside the HRV
autonomic adapter.
