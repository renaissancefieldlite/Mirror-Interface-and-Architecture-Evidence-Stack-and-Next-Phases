# Nest 3 Gases / Liquids / Phases Source Gate Plan

Date: `2026-05-26`

Status: `source_gate_executed / public_support_read_available`

## Lane

`Nest 3 / Gases / Liquids / Phases`

This lane tests whether thermophysical state rows preserve phase structure
across pressure, temperature, and measured property vectors. It should not be
collapsed into the RD-PCI water/plasma row or the oscillator rows; those are
adjacent supports, not this lane's phase-state gate.

## Primary Source

Primary source: `NIST Chemistry WebBook Thermophysical Properties of Fluid Systems`

Source page: `https://webbook.nist.gov/chemistry/fluid/`

Planned rows:

- pressure-temperature-property tables for real fluids
- liquid, vapor, saturation, and supercritical rows where source labels and
  ranges allow them
- property vectors such as density, enthalpy, entropy, heat capacity,
  viscosity, thermal conductivity, and speed of sound where available

## Planned State / Control

| Role | Planned definition |
| --- | --- |
| `target` | one phase state such as liquid, vapor, saturation, or supercritical |
| `control` | matched rows from another phase state for the same or held-out fluid family |
| `holdout` | species holdout, pressure-band holdout, or temperature-band holdout |
| `null` | property-family-only or range-only controls that test leakage |

## Planned Controls

- shuffled phase labels
- feature-shuffle control
- species holdout
- pressure / temperature holdout
- property-family control to ensure the read is not only a single obvious
  property column
- unit consistency and source-manifest check before scoring

## Public-Safe Output

Expected artifacts after execution:

```text
experiments/nest3_gases_liquids_phases_nist/run_nist_fluid_phase_gate.py
experiments/nest3_gases_liquids_phases_nist/results/nest3_gases_liquids_phases_nist_2026-05-26.json
docs/NEST3_GASES_LIQUIDS_PHASES_NIST_SUPPORT_READ_2026-05-26.md
```

Raw downloaded tables stay out of the public repo unless later cleared by
license, size, and public/private review. Public docs should cite the source,
fluid list, row count, phase definition, unit handling, controls, scores, and
boundary.

## Executed Support Read

The first source gate was executed on `2026-05-26`:

```text
docs/NEST3_GASES_LIQUIDS_PHASES_NIST_SUPPORT_READ_2026-05-26.md
```

The result is `support`.

## Boundary

This plan created the source gate and now points to the first support read.
The lane is not fully closed; supercritical / isobaric rows, pressure-band
holdouts, and multi-phase extension remain next gates.
