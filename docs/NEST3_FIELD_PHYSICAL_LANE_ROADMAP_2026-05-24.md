# Nest 3 Field / Physical Lane Roadmap

Date: `2026-05-24`

Status: `internal_work_order / real_data_only / mapped_continuation_until_scored`

## Point

This note keeps the full Lattice Companion scale visible while the current
B.A.S.I.S. / Nest 4 work continues. Phase 12C is a strong biology adapter and
B.A.S.I.S. product lane, but it is not the whole Nest map.

Nest 3 is the field / physical coherence layer. The goal is to move the mapped
lanes from roadmap language into real support rows:

```text
real source -> state/control -> transform -> drift controls -> score -> support read
```

No lane is support-bearing until it has a real dataset, capture, instrument
export, or public measurement source plus controls and a recorded score.

## Current Anchor

The Lattice Companion already seats Nest 3 as `Classical Coherence`.

Current known state:

- `Waves / Spectra / Phase-Lock`: first physical spectra support pass is seated
  through USGS ASTER-style spectra.
- `Hardware timing / coherence`: existing hardware timing rows support the
  timing/coherence direction.
- `Fire + Plasma`: first plasma optical-emission support row is seated through
  the RD-PCI nanosecond pulsed-discharge OES source.
- `EMF / Fields`: first waveform-state support row is seated through the
  RD-PCI VI pulse-coupled field source; time-order caveat remains.
- `Oscillators / Resonance`: public support chain is seated through NIST
  Luther phase/order, Silverbox forced-oscillator phase coupling, FASER
  forced-oscillation sweep rows, and FrID measured nonlinear
  frequency-response rows.
- `Fusion + Solar`: first NASA OMNIWeb / SPDF solar-plasma window support row
  is seated. It carries a distribution/window-statistic caveat because
  time-order-destroyed controls stayed high.
- `Gases / Liquids / Phases`: first NIST Chemistry WebBook thermophysical
  liquid/vapor support row is seated under species-held-out validation. It is
  not a full phase-diagram closeout yet.
- `Gravity / Orbits` and `Terahertz` remain mapped continuation lanes until
  dedicated real source packets are selected and scored. Adjacent rows may
  support parts of their bridge logic, but they are not standalone lane
  closeouts yet.

## Priority Lane Table

| Priority | Lane | Why it matters | First executable source gate | State / control idea | Output target |
| ---: | --- | --- | --- | --- | --- |
| `1` | `Native spectra / IR / Raman / THz` | Gives Nest 3 a second physical spectral family beyond the first spectra pass. | Select public IR, Raman, or THz spectral set. | material / molecule / water class vs wrong-class spectra; shuffled bands; null windows | `NEST3_SECOND_SPECTRAL_FAMILY_UDP_SUPPORT_READ` |
| `2` | `Fire + Plasma` | Tests high-energy reaction and field-regime dynamics without jumping to cosmic claims. | Select combustion emission, flame chemistry, plasma spectrum, or reaction-regime dataset. | flame/plasma regime vs baseline/wrong regime; shuffled wavelength or condition labels | `NEST3_FIRE_PLASMA_UDP_SUPPORT_READ` |
| `3` | `EMF / Fields` | Turns field language into measurable source-on/off, intensity, frequency, distance, or environmental field rows. | Use instrument source-on/off captures or public field measurement data. | source-on vs source-off; distance/intensity/frequency bands; time-shifted/null controls | `NEST3_EMF_FIELDS_UDP_SUPPORT_READ` |
| `4` | `Oscillators / Resonance` | Tests damping, forcing, entrainment, phase relation, and drift as real dynamics. | Use oscillator instrument row, public vibration/acoustic/pendulum/control dataset, or generated-from-instrument capture. | forced vs unforced; damped vs sustained; phase-lock vs shuffled phase | `NEST3_OSCILLATOR_RESONANCE_UDP_SUPPORT_READ` |
| `5` | `Fusion + Solar` | Bridges hydrogen/isotope, plasma, and solar output as observable physical systems. | NASA OMNIWeb / SPDF OMNI2 hourly solar-wind rows now executed. | active `Kp >= 5` windows vs quiet `Kp <= 2` windows; geomagnetic labels excluded from features | `NEST3_FUSION_SOLAR_OMNIWEB_SUPPORT_READ_2026-05-26` |
| `6` | `Gases / Liquids / Phases` | Tests thermodynamic phase/state behavior with pressure, temperature, density, and phase controls. | NIST Chemistry WebBook saturation fluid-property tables now executed. | saturated liquid vs vapor rows; species-held-out controls; pressure-temperature-only null | `NEST3_GASES_LIQUIDS_PHASES_NIST_SUPPORT_READ_2026-05-26` |
| `7` | `Gravity / Orbits` | Keeps orbit/resonance lane observable and public-data disciplined. | Select public ephemeris/orbit dataset. | orbital window vs shuffled orbit/time windows; resonance class vs null | `NEST3_GRAVITY_ORBITS_UDP_SUPPORT_READ` |
| `8` | `Terahertz cellular prototype` | Bridges physical spectra into water, biomolecules, cells, and DNA only after real THz/spectral source is seated. | Pair THz/spectral source with cellular or biomolecular response target. | exposure / spectral window vs baseline or wrong-window controls | `NEST3_THz_CELLULAR_BRIDGE_READ` |

## Execution Order

1. Close `Native spectra / IR / Raman / THz` first.
   This is the cleanest second physical family after the existing spectra pass.

2. Run `Fire + Plasma` next.
   It gives a visible high-energy lane with real regime controls and keeps the
   map from being reduced to biology.

3. Run `EMF / Fields` and `Oscillators / Resonance` as paired dynamics lanes.
   These are closest to the B.A.S.I.S. timing/coherence logic but must use
   physical captures or public measurements, not metaphor language.

4. `Fusion + Solar` first source gate is complete through NASA OMNIWeb / SPDF.
   Next layer: named storm / event-block holdouts, solar-cycle seasonal/null
   controls, and NASA POWER solar-radiation adjacency.

5. `Gases / Liquids / Phases` first source gate is complete through NIST
   saturation tables. Next layer: supercritical / isobaric rows,
   pressure-band holdouts, and multi-phase extension.

6. Keep `Gravity / Orbits`, `Terahertz`, and cosmic-scale rows as
   observable-data continuation lanes until dedicated source gates have scores.

## Support Language Rules

Use:

- `mapped continuation lane`
- `candidate source selected`
- `first UDP support read complete`
- `support-bearing after controls`
- `observable-data boundary`

Do not use:

- `validated`
- `closed`
- `proven universal`
- `field confirmed`
- `support-bearing`

unless the lane has source, state/control, transform, score, collapse controls,
and a recorded support read.

## Product / Claim Hooks

| Lane cluster | Product hook | Claim / evidence hook |
| --- | --- | --- |
| `Native spectra / THz / IR / Raman` | Golden Field Lite physical-spectra AI Expert; Mirror Architecture licensing for physical-state rows | Nested validation lane; physical observable support row; future FIG. support for external adapters |
| `Fire + Plasma / Fusion + Solar` | Quantum / energy / high-energy physics proof surface; NVIDIA PhysicsNeMo future adapter slot | Classical coherence / physical regime support; observable source-control rows |
| `EMF / Fields / Oscillators` | B.A.S.I.S. timing/coherence crosswalk; YRA Core instrument bench; edge-kit sensor experiments | Timing, phase, drift, source-on/off controls; instrument adapter support |
| `Gases / Liquids / Phases` | Materials / chemistry / environmental state expert | thermodynamic state/control rows; matter-to-field bridge |
| `Gravity / Orbits / Cosmic` | public-data observable comparator only | boundary lane until scored; no metaphysical overclaim |

## Next Clean Gate

Pick one source for the next unseated Nest 3 physical lane:

```text
Preferred next run: Gravity / Orbits public ephemeris/orbit dataset
Backup next run: Terahertz public spectral/exposure dataset
```

Then produce:

```text
source manifest
state/control table
feature transform note
score table
shuffled/null/wrong-class controls
public-safe support read
```
