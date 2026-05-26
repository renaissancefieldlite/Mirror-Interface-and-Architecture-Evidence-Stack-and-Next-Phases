# Next Nest Execution Outline

Date: `2026-05-24`

Status: `working_outline / next_run_order / real_data_only`

## Purpose

This is the next execution outline after the B.A.S.I.S. / Capital Connect side
quest. The goal is to finish the parked Nest work without letting Phase 12C
swallow the whole lattice map.

Current rule:

```text
roadmap rows do not become support rows until a real source, state/control
definition, transform, score, controls, and support read are recorded.
```

## Current Support Baseline

Already support-bearing or candidate-support:

- `Nest 4 / Cells + Genome`: WDBC morphology candidate support.
- `Nest 4 / Metabolism`: diabetes clinical/metabolic proxy candidate support.
- `Nest 2 / Food Chemistry`: USDA nutrient-composition bridge candidate support.
- `Nest 2 / Biomolecular Primitives`: ChEBI class/property and ChEBI ontology
  closure support rows.
- `Nest 3 / Waves-Spectra`: first physical spectra pass seated through USGS
  ASTER-style spectra.
- `Nest 3 / Waves-Spectra`: second physical spectral-family candidate support
  seated through NASA Ames Ramdb Raman transition tables; full raw-spectrum /
  phase-lock closeout remains open.
- `Nest 3 / Fire + Plasma`: first RD-PCI plasma OES source-gate support row
  completed; active pulse separates from late relaxation, but lane closeout
  needs stronger plasma-family or combustion controls.
- `Nest 3 / EMF / Fields`: first RD-PCI VI waveform-state support row
  completed; pulse-coupled field windows separate from far baseline controls.
  Oscillator / Resonance remains candidate because time-order shuffle stayed
  high.
- `Nest 3 / Oscillators / Resonance`: NIST Luther torsion-pendulum
  phase-order source gate completed. Real sequential oscillator windows
  separate from paired order-destroyed null windows while amplitude-only
  baseline stays at chance. Full lane closeout still needs repeated trials,
  forced/unforced labels, damping labels, or frequency sweeps.
- `Nest 3 / Oscillators / Resonance`: Silverbox forced-oscillator closeout
  completed. Repeated measured input/output windows from an electronic Duffing
  oscillator separate from circular-shifted, wrong-period, and phase-scrambled
  controls by coupling/phase features, while individual-signal baseline stays
  near chance on the clean combined packet.
- `Phase 12C / B.A.S.I.S.`: Muse / MoFit / Thermo active biology/device proof
  lane; raw captures remain private.

## Next Nest To Run

Run `Nest 3: Classical Coherence` next.

Reason:

- It prevents the project from over-fixating on B.A.S.I.S. / biology.
- It brings fire, plasma, spectra, fields, oscillators, and phase systems back
  into the full Lattice Companion scale.
- It creates a stronger bridge from matter / spectra into Golden Field Lite,
  PhysicsNeMo-style future adapters, and serious NVIDIA compute.

## Do Not Squash The Lane

Operator correction:

```text
Raman / IR / THz is the first executable support row, not the whole Nest 3 map.
```

The active Lattice Companion lane list remains:

| Companion lane | Current status | First clean gate |
| --- | --- | --- |
| `Terahertz` | mapped continuation | THz / IR / Raman spectral source or instrument export |
| `Fire + Plasma` | mapped continuation | combustion, flame-emission, plasma, or high-energy reaction dataset |
| `Fusion + Solar` | mapped continuation | solar / hydrogen / plasma-control source after fire-plasma pass |
| `Space / Time / Cycles` | mapped continuation | timing-window, periodicity, orbit, HRV/Muse, or hardware-cycle support table |
| `Gases / Liquids / Phases` | mapped continuation | NIST / phase / fluid / thermodynamic property rows |
| `Gravity / Orbits` | mapped continuation | public ephemeris, orbital-resonance, or gravity-observable comparator |
| `EMF / Fields` | mapped continuation | source-on/source-off field data or public field-measurement rows |
| `Oscillators / Resonance` | mapped continuation | oscillator, damping, entrainment, acoustic, vibration, or phase-lock row |
| `Waves / Spectra / Phase-Lock` | support-bearing plus continuation | second spectral family and phase-lock controls |

This outline starts with `Waves / Spectra / Phase-Lock` only because it is the
fastest real-data gate. It does not close or replace the other Nest 3 lanes.

## First Run: Second Physical Spectral Family

Preferred lane:

```text
Native spectra / IR / Raman / THz
```

Why first:

- cleanest Nest 3 continuation after the existing physical spectra pass
- real public datasets are likely available
- controls are straightforward
- it strengthens THz / water / molecule / cell bridge without overclaiming

Run packet:

| Field | Plan |
| --- | --- |
| `source` | public IR, Raman, THz, or native spectral dataset |
| `state` | material / molecule / water / mineral / organic class depending source |
| `control` | wrong-class spectra, shuffled labels, shuffled bands, null windows |
| `transform` | spectral windows, peak features, band ratios, derivative/shape features |
| `score` | AUC / AP / regression / support-state score depending label type |
| `failure mode` | observed signal collapses or controls do not separate from observed |
| `output` | `NEST3_SECOND_SPECTRAL_FAMILY_UDP_SUPPORT_READ_2026-05-24.md` or next dated run file |

### Source Hunt Result

Best first source:

```text
NASA Ames Ramdb: The NASA Raman Spectral Database
```

Why:

- primary NASA / NASA Ames source
- Raman spectra are a clean second physical spectral family after USGS ASTER
- raw and processed spectra are described as downloadable in CSV format
- sample families include amino acids, carbon allotropes, minerals, PAHs, and
  planetary / astrochemistry analogs
- gives a natural bridge from Nest 2 matter / biomolecular primitives into
  Nest 3 physical spectra

Source note:

```text
Ramdb paper: raw and processed Raman spectra can be downloaded from
www.astrochemistry.org/ramdb in CSV format.
```

Backup sources:

| Source | Role | Why not first |
| --- | --- | --- |
| `NIST Chemistry WebBook SRD 69` | broad IR / mass / UV/Vis / electronic-vibrational reference source | excellent official source, but bulk extraction may be slower and copyright / SRD use language needs careful handling |
| `NIST SRD 79 Quantitative Infrared Database` | small traceable quantitative IR pass | very clean NIST source but only 21 VOC absorption spectra, so better as a controlled micro-pass or calibration-style run |
| `AIST SDBS` | FT-IR + Laser Raman for organic compounds | strong resource, but daily/manual download limits and use constraints make it better as a later targeted confirmation |
| `MicrobioRaman / BioStudies` | biology-facing Raman lane | useful later for Nest 4 crossover, not the first Nest 3 physical-family pass |
| `THz concealed-object dataset` | THz imaging lane | THz imaging is useful, but less clean than spectral Raman for the first second-family read |

First executable choice:

```text
Run Ramdb Raman class separation first.
```

Executed support read:

```text
NEST3_RAMDB_RAMAN_UDP_SUPPORT_READ_2026-05-24.md
```

Executed hard controls:

```text
NEST3_RAMDB_RAMAN_HARD_CONTROLS_2026-05-24.md
```

Hard-control read:

- same-laser amino acid vs mineral remained support-bearing
- same-laser PAH vs amino acid remained support-bearing
- carbon allotrope vs mineral did not clear support at current sample size
- elevated band-position shuffles keep pure phase-lock / spectral-position
  closure open
- full raw / processed Ramdb CSV remains parked because the bundle is
  email-link gated by the Ramdb download form

Initial target/control ideas:

| Target | Control | Reason |
| --- | --- | --- |
| `amino acids` | `minerals` or `carbon allotropes` | biomolecular vs inorganic / carbon-structure separation |
| `PAHs` | `amino acids` | organic aromatic astrochemistry vs biomolecular primitive |
| `minerals` | `carbon allotropes` | material-family spectral separation |
| `raw spectra` | `processed spectra` | quality / preprocessing sensitivity check, not a main target |

## Second Run: Fire + Plasma

Preferred lane:

```text
combustion / flame emission / plasma spectra / high-energy reaction regime
```

Why second:

- directly answers the fire/plasma lattice gap
- makes the physical-field layer visually and technically clear
- creates a route into solar/fusion later without starting too cosmic

Run packet:

| Field | Plan |
| --- | --- |
| `source` | public combustion emission, flame chemistry, plasma spectrum, or regime dataset |
| `state` | flame/plasma regime, fuel/oxidizer condition, emission class, or reaction state |
| `control` | baseline/wrong regime, shuffled wavelength, wrong-condition labels, null windows |
| `transform` | spectral peaks, emission bands, time windows, condition descriptors |
| `score` | AUC / AP / correlation / regime separation |
| `failure mode` | high separation also appears under wrong/shuffled controls |
| `output` | `NEST3_FIRE_PLASMA_UDP_SUPPORT_READ_2026-05-24.md` or next dated run file |

Executed first source gate:

```text
NEST3_FIRE_PLASMA_RD_PCI_OES_SUPPORT_READ_2026-05-24.md
```

Executed read:

- source: RD-PCI / Ruhr University public time-resolved OES spectra for
  nanosecond pulsed discharges in distilled water
- target/control: active pulse `0-14 ns` vs late relaxation `20-34 ns`
- result: observed AUC `0.968750`, shuffled-label p `0.007968`,
  feature-shuffle AUC `0.218750`, band-shuffle AUC `0.796875`
- read: support-bearing first Fire + Plasma source gate
- boundary: not full Fire + Plasma closeout; stronger plasma-family controls
  and combustion / FTIR temperature spectra remain continuation gates

## Third Run: EMF / Fields + Oscillators

Run as paired dynamics lanes after one spectral and one high-energy lane.

Preferred source paths:

- source-on/source-off field measurement
- public EMF frequency/intensity/time dataset
- oscillator, vibration, acoustic, pendulum, damping, or forcing dataset
- instrument row from the local command center once hardware exists

Core controls:

- source-on vs source-off
- forced vs unforced
- damped vs sustained
- phase-lock vs shuffled phase
- time-shifted windows

Output targets:

- `NEST3_EMF_FIELDS_UDP_SUPPORT_READ`
- `NEST3_OSCILLATOR_RESONANCE_UDP_SUPPORT_READ`

Executed first paired source gate:

```text
NEST3_EMF_OSCILLATOR_RD_PCI_VI_SUPPORT_READ_2026-05-25.md
```

Executed read:

- source: RD-PCI / Ruhr University public VI waveform for nanosecond pulsed
  discharges in distilled water
- target/control: pulse-coupled field window `-100 ns` to `500 ns` versus far
  pre-baseline and late baseline
- result: full waveform features observed AUC `0.947917`, shuffled-label
  p `0.003984`, feature-shuffle AUC `0.444444`
- read: `EMF / Fields` waveform-state support
- caveat: within-window time-order shuffle stayed high (`AUC 0.972222`), so
  oscillator / resonance phase-order closeout remains open

Executed stricter oscillator / phase-order source gate:

```text
NEST3_OSCILLATOR_LUTHER_NIST_PHASE_ORDER_SUPPORT_READ_2026-05-25.md
```

Executed read:

- source: NIST Dataplot `LUTHER.DAT`, Newton's gravitational constant via
  torsion pendulum experiment
- target/control: real sequential torsion-pendulum windows versus paired
  order-destroyed null windows preserving the same amplitude distribution
- result: order/phase-only features observed AUC `1.000000`, shuffled-label
  p `0.003984`, feature-shuffle AUC `0.642538`
- guardrail: amplitude-only baseline AUC `0.500000`, shuffled-label
  p `0.450199`
- read: `Oscillators / Resonance` phase-order source-gate support
- caveat: single public trace; full lane closeout needs repeated trials,
  forced/unforced or damped/sustained labels, frequency sweeps, or local
  instrumented rows

Executed full forced-oscillator closeout:

```text
NEST3_OSCILLATOR_SILVERBOX_FORCED_CLOSEOUT_2026-05-25.md
```

Executed read:

- source: official Nonlinear Benchmark `Silverbox`, electronic Duffing
  oscillator input/output measurements
- target/control: aligned measured input/output windows versus
  circular-shifted, wrong-period, and phase-scrambled output controls
- clean combined result: coupling/phase features AUC `1.000000`, shuffled-label
  p `0.003984`, feature-shuffle AUC `0.510478`
- guardrail: individual-signal baseline AUC `0.529607`, p `0.119522`
- read: repeated-window forced-oscillator phase-coupling support
- caveat: next layer is local instrument rows or explicit frequency-sweep /
  forced-unforced / damped-sustained labels

## Deferred Nest 3 Rows

Do not run these first unless a clean source drops into the workspace:

| Lane | Status | Reason to defer |
| --- | --- | --- |
| `Fusion + Solar` | mapped continuation | run after fire/plasma or second spectral family is scored |
| `Gases / Liquids / Phases` | mapped continuation | good lane, but source selection needs care |
| `Gravity / Orbits` | observable-data boundary | keep rigorous; run after smaller physical rows |
| `Terahertz cellular bridge` | mapped continuation | needs both spectral source and cellular/biomolecular response target |
| `Cosmic rows` | observable-data boundary | do not start cosmic until Nest 3 smaller physical lanes score |

## Immediate Work Order

1. Keep the Ramdb raw-spectrum / phase-lock closeout parked until the
   email-gated CSV bundle or another continuous-spectrum source is available.
2. Choose the next physical lane by source cleanliness: `Fusion + Solar`,
   `Gases / Liquids / Phases`, `Gravity / Orbits`, or a harder
   `Oscillators / Resonance` dataset.
3. Build source manifest.
4. Define target/control classes.
5. Build feature extraction script or notebook.
6. Run observed score.
7. Run shuffled-label control.
8. Run feature-shuffle / band-shuffle / time-order or phase control.
9. Write support read with boundary language.
10. Patch Lattice Companion / public-safe summary only after the run exists.

## Public-Safe Language

Use:

```text
Nest 3 physical source-gate support read
```

or:

```text
candidate physical coherence support row
```

Do not use:

```text
validated fire/plasma
validated universal field
proven plasma bridge
closed physical nest
```

until scores and controls exist.

## Next Gate

Next exact gate:

```text
pick the cleanest remaining public source among Fusion + Solar,
Gases / Liquids / Phases, Gravity / Orbits, or a harder independent
Oscillators / Resonance dataset; then run the next dated Nest 3
support read with shuffled-label and feature/phase controls.
```
