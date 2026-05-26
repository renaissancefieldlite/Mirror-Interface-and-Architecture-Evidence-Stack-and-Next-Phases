# Nest 3 Oscillator / Resonance FASER Frequency-Sweep Gate

Date: `2026-05-25`

Run ID: `nest3_oscillator_faser_frequency_sweep_gate_2026-05-25`

Status: `real_data / forced_oscillation / frequency_sweep / reduced_wind_tunnel_readout`

## Source

Source page: `https://conservancy.umn.edu/items/4d2e8831-b97d-4e9a-9c5e-2796b449195d`

Downloaded files:

- `FASER Test 158 Forced Oscillation Reduced Data.zip`
- `FASER Test 158 Metadata.pdf`
- `Run Log Test 158.xls`

Description: FASER Test 158 forced-oscillation wind-tunnel dataset. Metadata states the reduced data are in MATLAB and text format and the run log details aircraft configuration and tunnel conditions for each run.

Metadata text extracted from the PDF states that the run log details aircraft
configuration and tunnel conditions, and that the forced-oscillation reduced
data are provided in MATLAB and text file format.

## State / Control

| Role | Definition |
| --- | --- |
| `target` | FASER forced-oscillation forcing setting labels: frequency or amplitude |
| `readout features` | coefficient surface summaries from `ca`, `cy`, `cn`, `cll`, `cm`, `cln` and inertia-corrected companions |
| `excluded from features` | run ID, tare, frequency, k, amplitude, nondimensional rate, qbar, velocity, alpha, beta |
| `control 1` | shuffled forcing labels |
| `control 2` | feature-column shuffle across runs |
| `control 3` | curve-order destruction inside each run while preserving coefficient distributions |

Tasks:

- `frequency_high_075_100_vs_lower_025_053`: High forcing frequency runs (0.75/1.0 Hz) versus lower forcing frequency runs (0.25/0.53 Hz). Explicit frequency/amplitude columns, run IDs, qbar, velocity, alpha, beta, and tare are excluded from the model features.
- `frequency_low_025_vs_mid_053`: Mid forcing frequency runs (0.53 Hz) versus low forcing frequency runs (0.25 Hz). Explicit frequency/amplitude columns, run IDs, qbar, velocity, alpha, beta, and tare are excluded from the model features.
- `frequency_mid_053_vs_high_075_100`: High forcing frequency runs (0.75/1.0 Hz) versus mid forcing frequency runs (0.53 Hz). Explicit frequency/amplitude columns, run IDs, qbar, velocity, alpha, beta, and tare are excluded from the model features.
- `amplitude_high_ge20_vs_low_le10`: High forcing amplitude runs (>=20 deg) versus low forcing amplitude runs (<=10 deg). Explicit frequency/amplitude columns, run IDs, qbar, velocity, alpha, beta, and tare are excluded from the model features.

## Data Shape

| Field | Value |
| --- | ---: |
| Usable reduced runs | 50 |
| Readout columns | 12 |

## Results

| Task | Records | Target/control | Features | Observed AUC | Balanced accuracy | Shuffled-label mean AUC | Shuffled-label p | Feature-shuffle AUC | Curve-order-destroyed AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `frequency_high_075_100_vs_lower_025_053` | 50 | 12/38 | 157 | 0.940536 | 0.840565 | 0.491765 | 0.003984 | 0.586607 | 0.797440 |
| `frequency_low_025_vs_mid_053` | 38 | 26/12 | 157 | 0.985000 | 0.927333 | 0.491966 | 0.003984 | 0.499000 | 0.827667 |
| `frequency_mid_053_vs_high_075_100` | 38 | 12/26 | 157 | 0.894000 | 0.833000 | 0.494497 | 0.003984 | 0.319000 | 0.693667 |
| `amplitude_high_ge20_vs_low_le10` | 40 | 11/29 | 157 | 0.916333 | 0.804500 | 0.496266 | 0.003984 | 0.365167 | 0.751000 |

## Interpretation

This is the stronger post-Silverbox gate for `Oscillators / Resonance`: a real
wind-tunnel forced-oscillation package with explicit frequency and amplitude
sweeps. The model does **not** receive frequency, amplitude, run, velocity,
qbar, alpha, beta, tare, or reduced-frequency columns. It only sees
force/moment readout-surface features.

Support criterion:

1. observed readout-surface AUC rises above shuffled-label controls;
2. feature-column shuffle degrades the result;
3. curve-order destruction helps distinguish whether the read is surface-shape
   / phase-order dependent or mostly distribution-level.

If the curve-order-destroyed AUC stays high, the result should be called a
forced-oscillation readout-surface support pass, not a full phase-order
closeout. If it drops, the task carries stronger curve-state support.

## Boundary

This is reduced wind-tunnel derivative data, not raw sensor waveforms and not a
local instrumented source-on/source-off capture. It is stronger than the
single-trace NIST phase-order pass because the labels are explicit
forced-oscillation frequency/amplitude settings, but the next best closeout
remains local source-on/source-off acquisition or a raw frequency-response
dataset with time traces.
