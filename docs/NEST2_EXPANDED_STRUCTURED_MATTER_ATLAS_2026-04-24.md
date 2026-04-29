# Nest 2 Expanded Structured Matter Atlas

Date: `2026-04-24`

Status:
expanded Nest 2 matter dictionary / `Engine 02` expanded pass

## Purpose

`Nest 2` core is already locked as the first constrained matter rung:

```text
elements -> molecular graphs -> H2O -> minerals / redox -> nutrition -> contaminants
```

This atlas expands that rung so the matter layer can support chemistry-facing,
materials-facing, food-facing, pharmaceutical-facing, water-facing,
pollutant-facing, and biology-facing representations without forcing every
lane into one overloaded bucket.

The shared score schema stays the same:

```text
state / control / transform / invariant / drift / coherence / score
```

## Expanded Lanes

| Lane | What It Adds | Main Invariants | Bridge |
| --- | --- | --- | --- |
| organic functional groups | alcohols, acids, amines, aromatics, carbonyls, fluorinated chains | bond order, heteroatom motif, reactivity family, substitution site | pharma, PFAS, food chemistry |
| biomolecular primitives | amino acids, nucleotides, lipids, sugars | sequence unit, charge / polarity, backbone, cellular role | chemistry into biology |
| polymers / plastics | polymer chains, microplastic fragments, PET, polyethylene | repeat unit, chain class, backbone, fragment endpoint | plastics and degradation pathways |
| electrochemistry | ions, batteries, conductivity, membranes, charge transfer | charge balance, redox pair, conductive path, membrane selectivity | cells, water, batteries, grids |
| catalysis / conditions | heat, pH, light, plasma, mineral surfaces, enzymes, catalysts | declared condition, pathway delta, endpoint selectivity, control separation | reaction optimization |
| spectral signatures | `IR`, Raman, `THz`, `NMR`, mass spec | peak family, mode assignment, baseline control, repeatable signature | measurement and Nest 3 resonance |
| environmental fate | soil, water, leaching, bioaccumulation, transformation products | medium context, transport path, descendant identity, risk endpoint | ecology and remediation |
| materials / semiconductors | crystals, defects, bands, phonons, lattice stability | unit cell, defect class, response family, stability relation | materials models and devices |

## Engine 02 Expanded Pass

The expanded pass is now represented in:

```text
tools/lattice_model_node_companion/engines/nest2_matter_engine.py
```

Generated report:

```text
tools/lattice_model_node_companion/outputs/nest2_matter_engine_report.md
```

The report now includes an `Expanded Nest 2 Lanes` table with the eight new
lanes, their bounded separation scores, bridges, and reads.

## What The Expanded Pass Shows

The expanded pass is a methodology result. It shows that `Nest 2` is not just
"chemistry" in the narrow sense; it is a structured-matter representation
dictionary.

It is the structured-matter dictionary for:

- molecular identity
- functional motif recovery
- charge / redox behavior
- polymer and fragment tracking
- measurement signatures
- environmental transport
- materials response
- biology-facing chemical primitives

This matters because the higher nests need a disciplined matter base:

- `Nest 3` needs spectra, fields, charge movement, catalysis, and resonance
- `Nest 4` needs amino acids, sugars, lipids, nucleotides, minerals, and
  hydration chemistry
- `Nest 5` needs environmental fate, material flows, soil / water behavior,
  and planetary-scale transport

## Core Finding

The core finding is narrower and cleaner than physical validation:

```text
the same scoring schema can be widened across structured-matter
representations
```

The same rule keeps holding:

```text
recover the family
preserve the graph / motif / lattice / pathway
respect conserved quantities
track drift and bad descendants
score against controls
```

That is the expanded matter methodology rung.

## Boundary

This is still a local methodology and comparator pass.

It is not a lab chemistry result, remediation result, nutrition claim,
medical claim, or materials-discovery claim.

It is the scaffold that tells us exactly what future chemistry, spectral,
materials, and biological data must prove.

## Beyond Initial Mapping

To move from real-data validation expansion into physical or experimental validation,
the next Nest 2 work must add:

- real periodic-table and molecular datasets
- real molecule parsing and fingerprints, such as `RDKit`
- measured spectral or assay data, such as `IR`, Raman, `THz`, `NMR`, or mass
  spectrometry
- explicit reaction products, descendants, and mass / charge balance
- declared controls for heat, pH, light, catalyst, plasma, or mineral surface
- external validation against known chemistry, materials, or environmental
  datasets

## Physical Validation Upgrade Path

The clean upgrade is:

```text
synthetic rows -> real dataset -> declared baseline -> locked score -> measured
property / known pathway / known stability comparison
```

Three practical validation lanes are available:

| Lane | Dataset / Tool Path | Testable Claim | Baseline |
| --- | --- | --- | --- |
| cheminformatics | `RDKit` plus public molecule datasets such as `QM9`, `ZINC`, or `ChEMBL` | Source Mirror Pattern score predicts known molecular property, stability, reactivity, or binding-related target better than a naive baseline | random features, simple fingerprint-only score, shuffled labels |
| contaminant / PFAS pathways | EPA / peer-reviewed degradation and remediation pathway data | bad-descendant penalty identifies known problematic transformation products that parent-disappearance metrics miss | parent-loss-only metric |
| minerals / materials | `pymatgen`, `ASE`, and materials databases such as Materials Project | lattice / charge / structure score recovers known stable structures above invalid or shuffled controls | random lattice, charge-imbalanced, or unstable controls |

Best first target:

`RDKit + QM9-style molecule property validation`

Reason:

- no hardware required
- public benchmark path exists
- falsifiable success metric is straightforward
- it upgrades `Engine 02` from schema demonstrator to real-data comparator
- it keeps the claim bounded while creating a credible physical-data bridge

The PFAS lane is the strongest mission-facing lane, but it should come after
the generic molecule-property validation because contaminant pathway data and
descendant scoring are more complex.

## Next Step

After this pass, there are two clean next moves.

Validation move:

```text
Engine 02V = RDKit / public molecule dataset validation pass
```

Nesting move:

```text
Engine 03 = oscillator / resonance / field dynamics
```

`Engine 03` should inherit the Nest 2 rows that already point upward:

- spectral signatures
- electrochemistry
- catalysis / plasma conditions
- terahertz bridge
- fusion / solar bridge
- phase and flow systems
