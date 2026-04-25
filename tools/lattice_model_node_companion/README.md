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
python3 tools/lattice_model_node_companion/lattice_model_node_demo.py
```

The script writes:

```text
tools/lattice_model_node_companion/outputs/lattice_model_node_demo.html
```

Open that HTML file in a browser to test the interactive map.

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

