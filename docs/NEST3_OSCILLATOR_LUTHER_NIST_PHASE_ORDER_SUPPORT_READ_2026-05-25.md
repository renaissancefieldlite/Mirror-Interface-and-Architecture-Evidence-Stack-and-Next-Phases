# Nest 3 Oscillator / Resonance NIST Luther Phase-Order Support Read

Date: `2026-05-25`

Run ID: `nest3_oscillator_luther_nist_phase_order_2026-05-25`

Status: `real_data / NIST / torsion_pendulum / oscillator_phase_order_gate`

## Source

Public dataset: `LUTHER.DAT`

Source page: `https://www.itl.nist.gov/div898/software/dataplot/data/LUTHER.DAT`

Description: NIST Dataplot LUTHER.DAT: Newton's gravitational constant via torsion pendulum experiment; response variable is pendulum angle; 989 observations.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | real sequential torsion-pendulum oscillator windows |
| `control` | paired order-destroyed null windows preserving each window's amplitude distribution |
| `boundary` | single real NIST trace; GroupKFold keeps paired real/null windows in the same fold |

## Data Shape

| Field | Value |
| --- | ---: |
| Source observations | 989 |
| Window size | 96 |
| Window step | 16 |
| Pairs | 56 |
| Records | 112 |
| Full feature count | 33 |
| Order / phase feature count | 19 |
| Amplitude-only feature count | 14 |

## Results

| Model | Features | Observed AUC | Balanced accuracy | Shuffled-label mean AUC | Shuffled-label p | Feature-shuffle AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `order_plus_amplitude_features` | 33 | 1.000000 | 1.000000 | 0.494589 | 0.003984 | 0.409758 |
| `order_phase_features_only` | 19 | 1.000000 | 1.000000 | 0.491412 | 0.003984 | 0.642538 |
| `amplitude_distribution_only_baseline` | 14 | 0.500000 | 0.500000 | 0.485973 | 0.450199 | 0.359694 |

## Interpretation

This is the stricter `Oscillators / Resonance` follow-up to the RD-PCI VI gate.
Instead of asking whether a large field event separates from quiet baseline, it
asks whether a real oscillator's sequential phase/order structure survives when
amplitude distribution is held constant.

The critical guardrail is the amplitude-only baseline. If amplitude-only
features score near chance while order / phase features score above shuffled
labels and feature shuffle, the support is phase/order-bearing rather than
simple amplitude distribution.

## Boundary

This is still a single public oscillator trace, so it should be read as a
phase-order source gate, not a full oscillator/resonance lane closeout. Stronger
continuation gates should use repeated oscillator trials, forced/unforced
conditions, damped/sustained labels, frequency sweeps, or instrumented local
source-on/source-off rows.
