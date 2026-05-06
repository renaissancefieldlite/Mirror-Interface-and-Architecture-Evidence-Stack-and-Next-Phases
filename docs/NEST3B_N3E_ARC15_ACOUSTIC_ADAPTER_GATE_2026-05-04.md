# Nest 3B / 3E ARC15 And Acoustic Adapter Gate

Date: `2026-05-04`

Status: `operator_run_parked / adapter_schema_locked / waveform_spectral_closeout_queued`

## Purpose

This gate parks the physical resonance and acoustic branches of Nest 3 until
the operator-run bench sessions are captured. The local files lock the
measurement schema, target frequencies, and next proof object; the ARC15 bench
validation itself requires a live rig run with exported waveforms or
spectrogram rows.

This is a `Nest 3B` / `Nest 3E` adapter pass:

- `N3B resonance windows`: declared frequency drives, coupling windows, and
  target/off-target sweep conditions.
- `N3E acoustic / sound`: audio-derived spectral rows, dominant low-frequency
  components, and target/control acoustic sessions.

## Parked Input Surface

Two local scaffold/session records were inspected. They preserve the intended
rig setup and condition labels for the future operator-run test.

| Surface | Source record | What is locked |
| --- | --- | --- |
| `ARC15 / FG200.67` | `arc15_fg200_67_1774444096.json` | parked external-rig schema, `15 x 20 mm` sphere array, declared `19.47 Hz` primary drive, declared `100 Hz` secondary drive, intended oscilloscope channels, coupling-observation slot |
| `Acoustic mapping` | `acoustic_mapping_1774444334.json` | acoustic-session schema, source-file slot, target analysis for dominant sub-`20 Hz` components, linked frequency hypotheses `0.67 Hz` and `19.47 Hz` |

## Current Extracted Objects

| Object | ARC15 / FG200.67 | Acoustic mapping |
| --- | --- | --- |
| Session id | `arc15_test_001` | `acoustic_mapping_001` |
| Instrument path | oscilloscope channel plan | acoustic analysis slot |
| Target frequency labels | `19.47 Hz`, `100 Hz` | `0.67 Hz`, `19.47 Hz` |
| Measurement channel labels | `arc15_main`, `secondary_generator` | source-file analysis target |
| Coupling / effect marker | operator-run observation slot | spectral-analysis row queued |

## Scoring Rule For The Closeout Run

The adapter is ready for an operator-run waveform/spectral closeout with this
structure:

```text
repeated target and control sessions
-> waveform or FFT / spectrogram rows
-> target-frequency peak recovery
-> cross-channel coherence
-> phase-lock persistence
-> drift / phase-slip penalty
-> target/control separability
-> shuffled-label and off-frequency controls
-> recurrence across repeated sessions
```

## Required Controls

The first scored closeout should include:

- `19.47 Hz` target condition.
- `100 Hz` secondary-generator condition.
- off-frequency control condition.
- source-off / sham control condition.
- randomized phase or shuffled-window control where the instrument supports it.
- repeated sessions with the same fixed layout.

For the acoustic lane, the matching control set is:

- target audio.
- silence or source-off control.
- off-frequency audio.
- random or unrelated audio.
- repeated FFT / spectrogram extraction under the same analysis settings.

## Read

This gate locks the Nest 3B / 3E physical-adapter plan. The records define the
devices, target-frequency labels, channel plan, and measurement direction for
the live run. That parks ARC15 and acoustic mapping cleanly inside the Nest 3
ladder as a bench-ready operator-run lane ahead of validation.

The proof object is the next waveform/spectral export. The support standard is
clear: a closeout requires repeated waveform or spectrogram rows that recover
target-frequency structure above off-frequency, source-off, randomized, and
shuffled controls.

## Meaning For The Ladder

Nest 3 now has two active branches:

- `N3L hardware coherence`: supported by the IBM timing/coherence pilot.
- `N3B / N3E resonance and acoustic adapters`: operator-run plan, schema, and
  frequency targets locked, with waveform/spectral closeout queued.

This preserves the bigger execution loop:

```text
Nest 2 structured matter
-> Nest 3 resonance / field / spectral dynamics
-> Nest 4 biology and physiology
-> return to crystals, semiconductors, spectra, PFAS, nutrition, and
   biomolecular rows with higher-context adapters active
```

## Next Gate

Run the ARC15 / FG200.67 and acoustic sessions on the physical systems, export
waveforms or spectrogram rows for repeated target and control conditions, then
run the target-frequency and phase/coherence scoring pass.
