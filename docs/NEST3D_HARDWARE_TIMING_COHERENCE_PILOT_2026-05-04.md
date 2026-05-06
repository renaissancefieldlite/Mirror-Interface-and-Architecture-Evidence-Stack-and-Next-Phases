# Nest 3D / 3L Hardware Timing-Coherence Pilot

Date: `2026-05-04`

Status: `hardware_coherence_baseline_supported / timing_window_closeout_open`

## Purpose

This is the first executed Nest 3 branch after the classical-coherence
readiness gate. It uses the local IBM timing-window surface because it already
contains repeated hardware records with declared timing labels.

The question is narrow:

```text
Do declared timing windows carry measurable hardware-coherence structure above
timing-blind and shuffled-window controls?
```

This is a `Nest 3D` / `Nest 3L` adapter run:

- `N3D phase-lock / timing`: declared timing windows and timing stability.
- `N3L hardware coherence`: target-subspace stability under hardware timing and
  noise variation.

## Input Surface

The pilot used three completed IBM timing-window sweep manifests.

| Input class | Value |
| --- | --- |
| Sweep count | `3` |
| Declared windows | `1.10`, `1.25`, `1.40`, `1.49`, `1.60`, `1.75`, `1.90` seconds |
| Capture rows | `168` |
| Shots per capture | `32` |
| Backend family | IBM hardware timing-window records |

## Metrics

Each capture was reduced to four public-safe metrics:

| Metric | Definition |
| --- | --- |
| `target_subspace_probability` | probability mass in the target Bell-style states, `P(00 or 11)` |
| `off_target_probability` | probability mass outside the target subspace |
| `bell_imbalance` | absolute imbalance between the two target states, `abs(P00 - P11)` |
| `coherence_stability_score` | `target_subspace_probability - off_target_probability - bell_imbalance` |

The pilot then compared declared timing-window groups against shuffled-window
controls.

## Results

| Metric | Result |
| --- | ---: |
| Rows scored | `168` |
| Mean target-subspace probability | `0.966145833` |
| Mean off-target probability | `0.033854167` |
| Mean Bell-state imbalance | `0.147321429` |
| Mean coherence-stability score | `0.784970238` |
| Window-label eta squared on stability score | `0.027311737` |
| Shuffled-window p-value for eta squared | `0.607078584` |
| Best timing window by mean stability score | `1.49 s` |
| Best-window delta over rest | `0.041232639` |
| Shuffled-window p-value for best-window delta | `0.391521696` |

Window-level stability scores:

| Window | Rows | Mean target-subspace probability | Mean coherence-stability score |
| --- | ---: | ---: | ---: |
| `1.10 s` | `24` | `0.9622` | `0.7695` |
| `1.25 s` | `24` | `0.9648` | `0.7539` |
| `1.40 s` | `24` | `0.9661` | `0.7943` |
| `1.49 s` | `24` | `0.9766` | `0.8203` |
| `1.60 s` | `24` | `0.9596` | `0.7747` |
| `1.75 s` | `24` | `0.9792` | `0.7943` |
| `1.90 s` | `24` | `0.9544` | `0.7878` |

## Read

The hardware-coherence branch is useful. Target-subspace probability stayed
high across the timing-window surface, with an overall mean of `0.966145833`.
That supports the use of this surface as a hardware-coherence adapter inside
Nest 3.

The timing-window label itself is still an open closeout. The best observed
window was `1.49 s`, and shuffled-window controls kept declared timing-window
separation queued for a sharper pass. The window-label effect size was small
(`eta squared = 0.027311737`) and the shuffled-window p-value was high
(`0.607078584`).

## Meaning For Nest 3

This pilot opens Nest 3 with a real hardware timing/coherence record, while
preserving the support standard:

- `N3L hardware coherence`: usable support surface.
- `N3D timing / phase-lock`: directional timing-window candidate, closeout
  open.
- `N3B / N3E resonance and acoustic lanes`: still need waveform / spectrogram
  exports.
- `N3F / N3G spectral and terahertz lanes`: still need measured spectra or
  assay-linked spectral rows.

## Next Gate

The next stronger Nest 3 run should use one of these richer surfaces:

1. ARC15 / FG200.67 waveform exports with repeated target, off-frequency, and
   sham sessions.
2. Acoustic FFT / spectrogram rows with repeated target and control sessions.
3. Public or partner spectral data such as IR, Raman, THz, NMR, or material
   spectra with condition labels.
4. A sharper hardware timing run with more shots, more repeats, and a locked
   target window before measurement.
