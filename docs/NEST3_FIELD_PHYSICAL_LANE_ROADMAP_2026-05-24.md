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

Closeout board:

- `FINAL_NEST_CLOSEOUT_BOARD_2026-07-14.md`
- `NEST3_BACKFILL_CLOSEOUT_VERIFICATION_2026-07-14.md`

## Current Anchor

The Lattice Companion already seats Nest 3 as `Classical Coherence`.

Current known state:

- `Waves / Spectra / Phase-Lock`: first physical spectra support pass is seated
  through USGS ASTER-style spectra, Raman has class-transition support, NIST
  THz has partial material-family support, NIST gas-phase IR has functional
  spectral-family support, and cross-spectral plus same-family spectral panels
  are now seated. Do not call pure phase-lock until raw phase controls or
  source-on/off instrument rows close it.
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
- `Fusion + Solar`: NASA OMNIWeb / SPDF solar-plasma window support is seated
  and hardened with storm/event-block holdouts plus seasonal/null controls. It
  remains window-statistic support, not raw phase-order support.
- `Gases / Liquids / Phases`: NIST Chemistry WebBook thermophysical support is
  seated across saturated liquid/vapor rows and hardened with isobaric
  supercritical rows. It is stronger phase-diagram support, not a complete
  thermodynamic atlas.
- `Gravity / Orbits`: first NASA Exoplanet Archive adjacent-orbit support row
  is seated. It is a first-pass orbit-architecture read, not a full dynamical
  resonance or ephemeris-propagation closeout.
- `Terahertz`: first NIST Chemistry WebBook THz spectral gate is seated. It is
  partial spectral-family support through the pharma-vs-non-pharma contrast;
  broad four-family material classification remains candidate. Same-family
  THz carbohydrate and inorganic rows add mixed support. A hard cross-material
  public source/reference transfer test was weak/null, but the repeated-scan
  THz-TDS gate using `30` Fe10nm-on-MgO sample scans vs `30` MgO reference scans
  is support-bearing for matched instrument source/reference separation with a
  nuisance caveat. A biological GEO panel now seats real THz exposure-response
  rows: `GSE178729` is support-bearing, `GSE248763`, `GSE41084`, and
  `GSE44671` are candidate, and `GSE243842`, `GSE41083`, and `GSE41085` are
  weak/null under the public-safe scorer. The harmonized THz biology manifest
  is complete, but same-platform probe, mouse gene-symbol, and mouse
  GO-process cross-source holdouts stayed weak/mixed. The full
  heat/off-window/frequency/power/duration/temperature control matrix remains
  open.

## Priority Lane Table

| Priority | Lane | Why it matters | First executable source gate | State / control idea | Output target |
| ---: | --- | --- | --- | --- | --- |
| `1` | `Native spectra / IR / Raman / THz` | Gives Nest 3 a multi-source physical spectral panel beyond the first spectra pass. | NIST Chemistry WebBook gas-phase IR spectra, NIST THz, NASA Ames Ramdb Raman, public THz-TDS source/reference traces, and public biological THz GEO rows now tied into cross-spectral, same-family, repeated-scan, manifest, and weak/mixed shared-feature panels. | family-heldout folds; same-family stress rows; sample/reference trace rows; biological manifest rows; shared-feature holdouts; shuffled labels; band-position/time-order shuffle; distribution-only controls | `NEST3_THZ_BIOLOGY_MANIFEST_SHARED_HOLDOUT_READ_2026-06-12.md` |
| `2` | `Fire + Plasma` | Tests high-energy reaction and field-regime dynamics without jumping to cosmic claims. | Select combustion emission, flame chemistry, plasma spectrum, or reaction-regime dataset. | flame/plasma regime vs baseline/wrong regime; shuffled wavelength or condition labels | `NEST3_FIRE_PLASMA_UDP_SUPPORT_READ` |
| `3` | `EMF / Fields` | Turns field language into measurable source-on/off, intensity, frequency, distance, or environmental field rows. | Use instrument source-on/off captures or public field measurement data. | source-on vs source-off; distance/intensity/frequency bands; time-shifted/null controls | `NEST3_EMF_FIELDS_UDP_SUPPORT_READ` |
| `4` | `Oscillators / Resonance` | Tests damping, forcing, entrainment, phase relation, and drift as real dynamics. | Use oscillator instrument row, public vibration/acoustic/pendulum/control dataset, or generated-from-instrument capture. | forced vs unforced; damped vs sustained; phase-lock vs shuffled phase | `NEST3_OSCILLATOR_RESONANCE_UDP_SUPPORT_READ` |
| `5` | `Fusion + Solar` | Bridges hydrogen/isotope, plasma, and solar output as observable physical systems. | NASA OMNIWeb / SPDF OMNI2 hourly solar-wind rows now executed and hardened. | active `Kp >= 5` windows vs quiet `Kp <= 2`; event-block holdouts; same-month / calendar null controls | `NEST3_FUSION_SOLAR_OMNIWEB_HARDENING_READ_2026-05-26.md` |
| `6` | `Gases / Liquids / Phases` | Tests thermodynamic phase/state behavior with pressure, temperature, density, and phase controls. | NIST Chemistry WebBook saturation and isobaric fluid-property tables now executed. | liquid/vapor/supercritical rows; species and species-pressure holdouts; feature/label shuffles | `NEST3_GASES_LIQUIDS_PHASES_NIST_HARDENING_READ_2026-05-26.md` |
| `7` | `Gravity / Orbits` | Keeps orbit/resonance lane observable and public-data disciplined. | NASA Exoplanet Archive adjacent multi-planet orbital rows now executed. | near low-order adjacent period-ratio resonance vs far off-resonance pairs; host-system holdout | `NEST3_GRAVITY_ORBITS_EXOPLANET_SUPPORT_READ_2026-05-26` |
| `8` | `Terahertz cellular prototype` | Bridges physical spectra into water, biomolecules, cells, and DNA only after real THz/spectral source is seated. | NIST Chemistry WebBook THz spectra, same-family carbohydrate/inorganic stress rows, repeated-scan THz-TDS sample/reference rows, GEO biological THz/control or THz/sham expression rows, and a harmonized biological THz manifest are seated; cross-source biological transfer remains weak/mixed. | material-family labels; repeated sample/reference scans; biological THz/control rows; exact label permutation; feature-identity shuffle; gene-block controls; shared-feature/pathway holdouts; missing heat/off-window/frequency/power/duration/temperature closeout | `NEST3_THZ_BIOLOGY_MANIFEST_SHARED_HOLDOUT_READ_2026-06-12.md` |

## Execution Order

1. `Native spectra / IR / Raman / THz` now has a first Terahertz source gate,
   a second NIST gas-phase IR source gate, and a cross-spectral family panel
   tying NIST IR, NIST THz, and NASA Ames Ramdb Raman rows together, plus a
   same-family stress panel. A hard public THz sample/reference transfer test
   was weak/null, then a repeated-scan THz-TDS source/reference gate landed as
   support-bearing for matched instrument separation. The next biological pass
   seated seven public GEO THz exposure-response rows: one support-bearing,
   three candidate, and three weak/null under controls. The harmonized
   manifest is now complete, and the stricter same-platform/gene/pathway
   cross-source holdouts stayed weak/mixed. Next layer is local/partner
   source-disabled rows or a fully matched public exposure matrix with sham,
   off-window, heat, frequency, power, duration, and temperature controls.

   Plain-English arc: the spectra lane now shows real public source structure,
   including harder same-family rows and repeated THz-TDS sample/reference
   scans. The biology-facing THz bridge now reaches real expression-response
   rows, but shared-feature/pathway transfer does not yet carry across public
   biological sources. It still needs a full physical-control matrix before it
   can be promoted beyond source-gate support.

2. Run `Fire + Plasma` next.
   It gives a visible high-energy lane with real regime controls and keeps the
   map from being reduced to biology.

3. Run `EMF / Fields` and `Oscillators / Resonance` as paired dynamics lanes.
   These are closest to the B.A.S.I.S. timing/coherence logic but must use
   physical captures or public measurements, not metaphor language.

4. `Fusion + Solar` first source gate and hardening loop are complete through
   NASA OMNIWeb / SPDF. Next layer: NASA POWER solar-radiation adjacency or a
   longer solar-cycle span with event-family holdouts.

5. `Gases / Liquids / Phases` first source gate and hardening loop are complete
   through NIST saturation and isobaric tables. Next layer: isochoric or
   two-phase dome rows, leave-one-pressure-band-out controls, and a second
   thermodynamic table family.

6. `Gravity / Orbits` first source gate is complete through NASA Exoplanet
   Archive adjacent planet-pair rows. Next layer: random-pair nulls,
   resonance-family holdouts, and a cleaner public ephemeris / orbit
   propagation source if available.

7. Keep cosmic-scale rows as observable-data continuation lanes until
   dedicated source gates have scores. Keep Terahertz cellular language bounded
   to the GEO exposure-response panel until the heat/off-window/frequency/
   power/duration/temperature controls are harmonized or locally captured.

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

Pick one source for the next unseated or under-hardened Nest 3 physical lane:

```text
Preferred next run: local/partner source-on/source-off THz/EMF rows with source-disabled baseline and environmental logging
Backup next run: fully matched public/partner THz biology matrix with sham/off-window, heat, frequency, power, duration, and temperature controls
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
