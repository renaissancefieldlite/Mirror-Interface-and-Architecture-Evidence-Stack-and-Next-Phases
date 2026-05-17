# Nest 2 Molecule Redox RedDB Support Read

Date: `2026-05-16`

Status: `public_safe_aggregate / real_reddb_dataset / no_raw_rows_published / no_code`

## Purpose

This pass seats the molecule-level redox follow-up after the NASA
Electrochemistry / Redox battery-aging row. NASA seated the device-aging side.
RedDB v2 seats the electroactive-molecule side by testing whether reactant /
product molecular structure carries reaction-energy and orbital-shift readouts
above shuffled controls.

## Source

- Source: RedDB, a computational database of electroactive molecules for
  aqueous redox flow batteries
- Dataverse DOI: `10.7910/DVN/F3QFSQ`
- Source table: `RedDBv2_reaction.tab`
- Reaction rows parsed: `15,882`
- Valid SMILES feature rows: `15,882`
- Grouped molecular-pair groups: `54`
- Shuffled controls: `250`

RedDB contains quinone and aza-aromatic electroactive molecules for aqueous
redox-flow-battery chemistry. The public Dataverse release provides reaction
rows with reactant/product SMILES, reaction energies, solubility values, and
HOMO/LUMO electronic quantities.

## State Map

| Variable | Molecule redox expression |
| --- | --- |
| `state` | reactant/product structural pair, reaction energy, HOMO/LUMO shifts |
| `control` | shuffled reaction-energy and orbital-shift targets |
| `transform` | reactant/product SMILES -> descriptors + fingerprints -> redox readout |
| `drift` | functional-group substitutions, bond type, solubility, redox-state shift |
| `quality` | real RedDB v2 reaction rows with valid RDKit-parsed SMILES |
| `support` | grouped held-out molecular-pair metrics against shuffled controls |

## Reaction-Energy Recovery

- target: `reaction_energy`
- rows: `15,744`
- grouped train/test rows: `10,899` / `4,845`
- Pearson: `0.881991`
- R2: `0.712436`
- RMSE: `0.025717`
- baseline RMSE: `0.048291`
- RMSE improvement: `0.467455`
- shuffled abs Pearson mean: `0.011135`
- shuffled abs Pearson p95: `0.027485`
- p(Pearson >= real): `0.003984`

Read:

```text
Reactant/product molecular structure recovers RedDB reaction-energy state
above shuffled controls. The p-value is at the 250-permutation floor.
```

## Orbital-Shift Recovery

HOMO shift:

- rows: `15,346`
- Pearson: `0.736113`
- R2: `0.346634`
- RMSE improvement: `0.258368`
- shuffled abs Pearson p95: `0.028461`
- p(Pearson >= real): `0.003984`

LUMO shift:

- rows: `15,346`
- Pearson: `0.530190`
- R2: `0.218085`
- RMSE improvement: `0.160525`
- shuffled abs Pearson p95: `0.028757`
- p(Pearson >= real): `0.003984`

Read:

```text
The molecule pair also carries electronic orbital-shift structure. HOMO shift
is the stronger orbital support row; LUMO shift clears shuffled controls as a
secondary electronic-response row.
```

## Descriptor Context

Solubility shift cleared shuffled Pearson controls but did not recover the
held-out magnitude cleanly:

- Pearson: `0.272168`
- R2: `-0.921847`
- p(Pearson >= real): `0.003984`

This row remains descriptor context for the molecule-redox lane. The promoted
support rows are reaction energy, HOMO shift, and LUMO shift.

## Meta Analysis

The RedDB pass adds a second Electrochemistry / Redox surface:

- NASA battery aging = device-level electrochemical state and impedance drift.
- RedDB molecule redox = molecule-level electroactive reaction and orbital
  shifts.

Both use real public datasets, held-out scoring, and shuffled controls. RedDB
therefore tightens the redox lane beyond battery aging and gives Nest 2 another
chemical substrate carrying the same state/control/transform/drift/quality
support stack.

## Cross-Nest Role

- `Nest 2`: seats molecule redox as a real electroactive-chemistry support
  row.
- `Nest 3`: prepares the bridge to cyclic-voltammetry and waveform/frequency
  electrochemistry.
- `Nest 5`: adds a molecule-redox support-state card beside battery aging,
  H2O, minerals, materials, and spectra.
- `FIG.14 / FIG.15`: strengthens external adapter and support-state routing
  examples for claims `26-30`.

## Public / Private Boundary

Public-safe: source identity, row counts, grouped split summary, aggregate
metrics, state map, support read, and continuation gates.

Private: downloaded RedDB source tables, feature matrices, runnable scripts,
local workbench outputs, and raw rows.

## Next Gate

```text
RedDB molecule redox seated
-> add DUCK/CV or another cyclic-voltammetry waveform dataset
-> improve EIS continuous-SOH gate
-> add molecule-redox support card to Nest 5 / Mirror Index
```
