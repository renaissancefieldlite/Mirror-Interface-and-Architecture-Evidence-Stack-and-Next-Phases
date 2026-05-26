# Nest 3 Fire + Plasma RD-PCI OES Support Read

Date: `2026-05-24`

Run ID: `nest3_fire_plasma_rd_pci_oes_2026-05-24`

Status: `real_data / RD-PCI / plasma_emission_spectra / support_with_source_gate_boundary`

## Source

Public dataset: `Continuum Spectra (dt =2ns) - Nanosecond pulsed discharges in distilled water - Part I: Continuum radiation and plasma ignition`.

Source page: `https://rdpcidat.rub.de/dataset/nanosecond-pulsed-discharges-distilled-water-part-i-continuum-radiation-and-plasma-0`

CSV: `https://rdpcidat.rub.de/sites/default/files/SFB1316_B7_2020_D1_R1_OES.csv`

The dataset page describes time-resolved emission spectra from the first `34 ns` after plasma ignition for a nanosecond pulsed plasma with approximately `15 ns` pulse width, `2-3 ns` rise time, `20 kV`, and `15 Hz`.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | active pulse window, `0-14 ns` |
| `control` | late relaxation window, `20-34 ns` |
| `held out` | `16 ns` and `18 ns` transition window; source columns beyond first stated `34 ns` not used |

## Results

| Metric | Value |
| --- | ---: |
| Wavelength points | 1744 |
| Source spectra columns | 30 |
| Used records | 16 |
| Features | 77 |
| Target / control records | 8 / 8 |
| Observed ROC AUC | 0.968750 |
| Observed balanced accuracy | 0.812500 |
| Shuffled-label mean AUC | 0.467500 |
| Shuffled-label p | 0.007968 |
| Feature-shuffle AUC | 0.218750 |
| Band-shuffle AUC | 0.796875 |

## Interpretation

This is a first executable `Nest 3 / Fire + Plasma` source gate. It tests whether time-window state in real plasma emission spectra separates active pulse behavior from late relaxation behavior.

Read as `support`.

## Boundary

This does not close the full Fire + Plasma lane. It is a small, real source-gate support read on time-resolved plasma optical emission spectra. Fire/combustion FTIR and stronger plasma-family controls remain continuation gates.

Dryad Minatre charcoal FTIR fire-temperature data remains a strong continuation candidate, but its file endpoint returned access-gated responses through the shell path during this run; keep it as a source gate, not an executed result yet.
