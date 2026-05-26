# Nest 3 Oscillator / Resonance Silverbox Forced-Oscillator Closeout

Date: `2026-05-25`

Run ID: `nest3_oscillator_silverbox_forced_closeout_2026-05-25`

Status: `real_data / forced_oscillator / repeated_windows / phase_coupling_closeout`

## Source

Official benchmark page: `https://sites.google.com/view/nonlinear-benchmark/benchmarks/silverbox`

Downloaded bundle: `https://drive.google.com/file/d/17iS-6oBUUgrmiAcrZoG9S5sOaljZnDSy/view`

Description: Official Nonlinear Benchmark Silverbox data. Silverbox is an electronic implementation of the Duffing oscillator; the downloaded bundle includes SNLS80mV.csv and Schroeder80mV.csv input/output measurements.

Local files:

- `Schroeder80mV.csv`
- `SNLS80mV.csv`
- `README.txt`

The bundle README states that `Schroeder80mV` contains a Schroeder-phase
multisine measurement and identifies a 1024-point period. This run uses the
available measured input/output CSVs as repeated forced-oscillator windows.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | aligned measured input/output windows from the forced Silverbox oscillator |
| `control 1` | same input with circularly shifted output |
| `control 2` | same input with wrong-period output |
| `control 3` | same input with phase-scrambled output |
| `diagnostic control` | same input with fully order-destroyed output |
| `guardrail` | individual-signal baseline using only input/output amplitude and spectrum features |

## Data Shape

| Field | Value |
| --- | ---: |
| Window size | 1024 |
| Window step | 1024 |
| Coupling / phase features | 23 |
| Individual-signal baseline features | 20 |

Records by test:

| Test | Records |
| --- | ---: |
| `aligned_vs_circular_shifted_output` | 512 |
| `aligned_vs_wrong_period_output` | 512 |
| `aligned_vs_phase_scrambled_output` | 512 |
| `aligned_vs_order_destroyed_output` | 512 |
| `clean_combined_forced_oscillator_controls` | 1024 |
| `combined_forced_oscillator_controls` | 1280 |

## Results

| Test / Feature Set | Records | Target/control | Features | Observed AUC | Balanced accuracy | Shuffled-label mean AUC | Shuffled-label p | Feature-shuffle AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `aligned_vs_circular_shifted_output__coupling_phase_features` | 512 | 256/256 | 23 | 1.000000 | 1.000000 | 0.498302 | 0.003984 | 0.496109 |
| `aligned_vs_circular_shifted_output__individual_signal_baseline` | 512 | 256/256 | 20 | 0.511551 | 0.505859 | 0.493457 | 0.346614 | 0.527435 |
| `aligned_vs_wrong_period_output__coupling_phase_features` | 512 | 256/256 | 23 | 1.000000 | 0.998047 | 0.496462 | 0.003984 | 0.467880 |
| `aligned_vs_wrong_period_output__individual_signal_baseline` | 512 | 256/256 | 20 | 0.371429 | 0.396484 | 0.494529 | 1.000000 | 0.502289 |
| `aligned_vs_phase_scrambled_output__coupling_phase_features` | 512 | 256/256 | 23 | 1.000000 | 1.000000 | 0.497180 | 0.003984 | 0.492966 |
| `aligned_vs_phase_scrambled_output__individual_signal_baseline` | 512 | 256/256 | 20 | 0.595657 | 0.541016 | 0.494539 | 0.003984 | 0.530212 |
| `aligned_vs_order_destroyed_output__coupling_phase_features` | 512 | 256/256 | 23 | 1.000000 | 1.000000 | 0.496618 | 0.003984 | 0.486679 |
| `aligned_vs_order_destroyed_output__individual_signal_baseline` | 512 | 256/256 | 20 | 1.000000 | 1.000000 | 0.493383 | 0.003984 | 0.531143 |
| `clean_combined_forced_oscillator_controls__coupling_phase_features` | 1024 | 256/768 | 23 | 1.000000 | 1.000000 | 0.496239 | 0.003984 | 0.510478 |
| `clean_combined_forced_oscillator_controls__individual_signal_baseline` | 1024 | 256/768 | 20 | 0.529607 | 0.523438 | 0.496644 | 0.119522 | 0.502253 |
| `combined_forced_oscillator_controls__coupling_phase_features` | 1280 | 256/1024 | 23 | 1.000000 | 0.999512 | 0.499205 | 0.003984 | 0.460201 |
| `combined_forced_oscillator_controls__individual_signal_baseline` | 1280 | 256/1024 | 20 | 0.641899 | 0.635742 | 0.497192 | 0.003984 | 0.525341 |

## Interpretation

This is the full `Oscillators / Resonance` closeout pass after the NIST Luther
single-trace phase-order gate. Silverbox gives a real forced oscillator with
measured input and output, so the test can ask whether the aligned forcing /
response relation survives against phase-shifted, wrong-period, and
order-destroyed controls.

Clean closeout read: the `clean_combined_forced_oscillator_controls` packet
passes the closeout criterion. Coupling / phase features score AUC `1.000000`
while shuffled-label and feature-shuffle controls degrade toward chance, and
the individual-signal baseline stays low (`AUC 0.529607`, p `0.119522`). This
supports repeated-window forced-oscillator phase-coupling rather than simple
amplitude or spectrum separation.

The closeout criterion is:

1. coupling / phase features separate aligned windows from null controls;
2. shuffled-label and feature-shuffle controls degrade the read;
3. individual-signal amplitude / spectrum baselines do not carry the clean
   controls.

If those three conditions hold, the lane can be called repeated-window
forced-oscillator phase-coupling support rather than simple amplitude or
single-trace order support. The fully order-destroyed permutation is retained
as a destructive diagnostic only; if its individual-signal baseline rises, that
does not invalidate the clean closeout controls because the permutation changes
the output's own spectrum/derivative structure.

## Boundary

This is still public benchmark data, not a local instrument row. The next
stronger layer is local source-on/source-off acquisition or an external
frequency-sweep dataset with explicit forced/unforced, damped/sustained, or
frequency-response labels.
