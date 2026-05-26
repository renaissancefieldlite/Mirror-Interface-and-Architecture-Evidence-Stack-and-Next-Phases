# Nest 3 EMF / Oscillator RD-PCI VI Support Read

Date: `2026-05-25`

Run ID: `nest3_emf_oscillator_rd_pci_vi_2026-05-25`

Status: `real_data / RD-PCI / VI_waveform / source_gate_support`

## Source

Public dataset: `VI Curve - Nanosecond pulsed discharges in distilled water - Part I: Continuum radiation and plasma ignition`.

Source page: `https://rdpcidat.rub.de/dataset/nanosecond-pulsed-discharges-distilled-water-part-i-continuum-radiation-and-plasma-1`

CSV: `https://rdpcidat.rub.de/sites/default/files/SFB1316_B7_2020_D1_R2_VI.csv`

The dataset page describes a VI curve measured with a BCS for a `12 m` cable, with columns for time, signal amplitude, shunt current, and voltage.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | pulse-coupled field window, `-100 ns` to `500 ns` |
| `control` | far pre-baseline plus late baseline windows |
| `boundary` | single-trace source gate; transition / near-tail windows excluded |

## Data Shape

| Field | Value |
| --- | ---: |
| Source rows | 400002 |
| Used windows | 36 |
| Target / control windows | 12 / 24 |
| Full feature count | 46 |
| Dynamics feature count | 25 |

## Results

| Model | Features | Observed AUC | Balanced accuracy | Shuffled-label mean AUC | Shuffled-label p | Feature-shuffle AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `full_emf_waveform_features` | 46 | 0.947917 | 0.875000 | 0.481542 | 0.003984 | 0.444444 |
| `dynamics_shape_features` | 25 | 0.774306 | 0.666667 | 0.472931 | 0.007968 | 0.447917 |
| `within_window_time_order_shuffle` | 46 | 0.972222 | 0.895833 | 0.504597 | 0.003984 | 0.607639 |

## Interpretation

This is a first executable paired `EMF / Fields + Oscillators / Resonance` source gate.

The full waveform model is support-bearing: real current / voltage / amplitude windows separate pulse-coupled field behavior from far baseline, and shuffled labels plus feature shuffle degrade the read.

The dynamics-only model is candidate support: it remains above shuffled labels, but it is weaker than the full waveform read.

The within-window time-order shuffle stays high. That means this pass should be read primarily as `EMF / Fields` waveform-state support. It does not yet prove oscillator / resonance dependence on temporal order or phase. Oscillator / resonance stays open for repeated traces, forced/damped oscillator data, source-on/source-off sessions, shielded/null controls, or phase-aware measurements.

## Boundary

This does not close the full EMF or Oscillator lanes. It is a single public VI trace source gate. Stronger continuation gates should use repeated traces, source-on/source-off sessions, shielded/null controls, or independently labeled forced/damped oscillator datasets.
