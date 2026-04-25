# Cleveland Clinic: Allosteric Signal Propagation

Track:
Unlocking Undruggable Targets: Quantum Simulation of Allosteric Signal
Propagation

## Enterprise Need

Cleveland Clinic needs credible computational paths for allosteric signaling
and difficult biological targets where classical simulation, structure, and
signal-propagation methods are under pressure.

## Mirror Architecture Fit

Primary nest:
`Nest 2 -> Nest 4`

State object:

- protein graph
- residue network
- binding pocket
- allosteric site
- conformational state
- signal-propagation path
- cell-context readout where available

Control:

- shuffled residue graph
- decoy ligand / inactive site
- random pathway
- known inactive mutation

Invariant:

- conserved fold relation
- active-site communication
- pathway continuity
- bounded conformational transition

Drift:

- false allosteric path
- misfold
- off-target pathway
- unstable conformer
- biological overclaim

## Local Predecessor Engine

Engine priority:
`Engine 02` Nest 2 matter / chemistry model plus `Engine 04` biology model

First local build:

- protein / residue graph comparator
- pathway preservation score
- perturbation vs control comparison
- small allostery map that can be visualized in the companion

## Quantum-Enabled Fork

Candidate methods:

- quantum simulation of small constrained conformational fragments
- hybrid quantum-classical pathway scoring
- quantum kernel over residue-path states
- Braket / Classiq toy benchmark before larger biological claim

## PoC Demonstrator

Show:

`protein graph -> perturbation -> allosteric path -> invariant pathway score -> drift / false-path penalty`

This track should stay biologically serious and bounded.

The win condition is not "solves biology."

The win condition is a credible allostery propagation comparator with a
quantum-enabled fragment test.

