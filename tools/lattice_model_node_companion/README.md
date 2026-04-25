# Lattice Model Node Companion

Date: `2026-04-24`

Status:
local browser demo / no external model calls

## Purpose

The Lattice Model Node Companion is the visual code lane for the Mirror
Architecture nesting work.

It turns the written nest maps into an explorable browser surface:

- one unified Mirror Architecture center
- `Nest 1` formal systems
- `Nest 2` structured matter, chemistry, food, and materials
- `Nest 3` fields, resonance, plasma, fusion, solar, and dynamics
- `Nest 4` biology, HRV, EEG, cells, genome, metabolism, and physiology
- `Nest 5` convergence systems
- adapter slots for later physics/material/natural-science models

The first build is deliberately lightweight. It does not call APIs, spend
credits, download models, or require NVIDIA / Hugging Face packages.

## Run

From the repository root:

```bash
tools/lattice_model_node_companion/run_demo.sh
```

The script writes the browser demo and the first local engine report:

```text
tools/lattice_model_node_companion/outputs/lattice_model_node_demo.html
tools/lattice_model_node_companion/outputs/nest1_formal_engine_report.json
tools/lattice_model_node_companion/outputs/nest1_formal_engine_report.md
tools/lattice_model_node_companion/outputs/nest2_matter_engine_report.json
tools/lattice_model_node_companion/outputs/nest2_matter_engine_report.md
```

Open that HTML file in a browser to test the interactive map.

## Local Engine Build Order

The companion now separates the visible chassis from the engines that can be
bolted in locally.

1. `Engine 00`: lattice console, built
2. `Engine 01`: `Nest 1` formal invariant model, built
3. `Engine 02`: `Nest 2` matter / chemistry / nutrition model, built
4. `Engine 03`: `Nest 3` coherence / physics model, planned
5. `Engine 04`: `Nest 4` biology / biosignal model, planned
6. `Engine 05`: `Nest 5` convergence model, planned

This is the demo answer when someone asks what is built:

the browser companion is the chassis, `Engine 01` demonstrates the formal
invariant grammar, and `Engine 02` demonstrates the first structured-matter
grammar across elements, molecular graphs, water, minerals, nutrition, redox,
and contaminant-pathway scoring without API calls.

## Future Adapter Slots

Later adapters can plug into the same node schema:

- `PhysicsNeMo`: physics surrogate / PDE / field-system adapter
- `MatterGen`: inorganic material candidate-generation adapter
- `MatGL / CHGNet / MACE`: atomistic graph and materials-property adapters
- `FairChem / Open Catalyst`: catalyst and reaction-surface adapter
- `RDKit / ASE / pymatgen`: molecule, atomistic, and crystal-structure tooling
- `HRV / EEG`: live human-state adapter

The rule is simple: first make the map legible, then plug in heavier models
only where they add real measurement or simulation value.
