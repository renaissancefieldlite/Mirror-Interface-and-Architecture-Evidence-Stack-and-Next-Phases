# Nest 3 Oscillator / Resonance FrID Clamped Frequency-Response Gate

Date: `2026-05-26`

Run ID: `nest3_oscillator_frid_clamped_frequency_response_gate_2026-05-26`

Status: `real_data / forced_response / measured_lvm / frequency_response_surface`

## Source

Source page: `https://zenodo.org/records/13305097`

Source DOI: `https://doi.org/10.5281/zenodo.13305097`

Downloaded files:

- `ClampedOsci.zip`
- `frid_zenodo_13305097.json`

Description: FrID: Frequency response based identification. Zenodo record 13305097. The ClampedOsci package contains measured forced-response sweeps for the oscillator with clamping nonlinearities studied in Breunung and Balachandran (2024), Journal of Sound and Vibration.

The local zip MD5 matches the Zenodo API checksum for `ClampedOsci.zip`: `0c97b222c71764ffe2629a3782edb521`.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | explicit forced-response amplitude or frequency state |
| `readout features` | measured response channels `V_acc` and `Strain_0` through `Strain_6` |
| `excluded from features` | file name, segment index, explicit amplitude, explicit frequency, shaker-control input, noise fields, comments |
| `grouping` | amplitude gates hold out frequency groups; frequency gate holds out amplitude groups |
| `control 1` | shuffled labels |
| `control 2` | feature-column shuffle across records |
| `control 3` | distribution-only feature set |
| `control 4` | time-order-destroyed response rows |

Tasks:

- `amplitude_2p0_vs_0p5_frequency_heldout`: High forcing amplitude 2.0 versus low forcing amplitude 0.5, with frequency groups held out.
- `amplitude_high_1p5_2p0_vs_low_0p5_1p0_frequency_heldout`: High forcing amplitudes 1.5/2.0 versus low forcing amplitudes 0.5/1.0, with frequency groups held out.
- `frequency_high_quartile_vs_low_quartile_amplitude_heldout`: High frequency quartile >= 47.240 Hz versus low frequency quartile <= 45.740 Hz, with amplitude groups held out.

## Data Shape

| Field | Value |
| --- | ---: |
| Measured LVM files | 4 |
| Parsed forced-response segments | 7078 |
| Response channels | `V_acc`, `Strain_0`, `Strain_1`, `Strain_2`, `Strain_3`, `Strain_4`, `Strain_5`, `Strain_6` |
| Frequency range | 45.000000 to 48.000000 Hz |
| Amplitude values | 0.5, 1.0, 1.5, 2.0 |

## Results

| Task | Records | Target/control | Groups | Features | Observed AUC | Balanced accuracy | Shuffled-label mean AUC | Shuffled-label p | Feature-shuffle AUC | Distribution-only AUC | Time-order-destroyed AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `amplitude_2p0_vs_0p5_frequency_heldout` | 3538 | 1771/1767 | 151 | 177 | 1.000000 | 1.000000 | 0.500672 | 0.003984 | 0.526514 | 1.000000 | 1.000000 |
| `amplitude_high_1p5_2p0_vs_low_0p5_1p0_frequency_heldout` | 7078 | 3533/3545 | 151 | 177 | 1.000000 | 1.000000 | 0.499204 | 0.003984 | 0.501185 | 1.000000 | 1.000000 |
| `frequency_high_quartile_vs_low_quartile_amplitude_heldout` | 3588 | 1794/1794 | 4 | 177 | 0.856880 | 0.791806 | 0.500573 | 0.003984 | 0.514505 | 0.695644 | 0.687492 |

## Interpretation

This is the stronger post-FASER oscillator continuation: real measured frequency-response sweeps from a nonlinear clamped oscillator. The model does not receive the explicit amplitude/frequency state columns or the shaker-control input. It only sees measured response-channel summaries and response coupling features.

The amplitude tasks are intentionally easy because forcing amplitude is visible
in response magnitude; distribution-only and time-order-destroyed controls stay
at `1.000000`, so those rows are magnitude-surface support, not phase/order
support. The frequency quartile task is the more useful continuation read:
it holds out amplitude groups and still scores `0.856880` AUC while feature
shuffle drops near chance (`0.514505`).

Support criterion:

1. observed response-surface AUC rises above shuffled-label controls;
2. feature-column shuffle degrades the result;
3. frequency or amplitude grouping prevents a simple train/test reuse of the same setting;
4. distribution-only and time-order-destroyed controls show whether the read is response magnitude / spectral structure or stronger time-order coupling.

If distribution-only or time-order-destroyed controls stay high, the lane should be called measured forced-response surface support rather than pure phase-order closeout. Silverbox remains the cleaner phase-coupling closeout; FrID adds real measured nonlinear oscillator frequency-response amplitude and frequency rows.

## Boundary

This gate uses public measured LabVIEW response sweeps, not local instrumented source-on/source-off hardware rows. It is appropriate for the `Oscillators / Resonance` and `Gases / Liquids / Phases` adjacency map only as oscillator frequency-response support. The next best hardware-facing gate remains local instrumented source-on/source-off rows or a measured damped/undamped transition dataset with null instrumentation.
