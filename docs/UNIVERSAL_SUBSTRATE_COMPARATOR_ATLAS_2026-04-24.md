# Universal Substrate Comparator Atlas

Date: `2026-04-24`

Status:
research-design atlas / not a completed proof map

## Purpose

This atlas expands the nesting ladder into a broader map of systems where the
Mirror Architecture score logic can be tested.

The point is not to claim that every domain is already proven. The point is to
make the project legible as a universal comparator program:

Can the same higher-order score logic be mapped across different substrates
when each substrate is allowed to express structure, drift, coherence, and
state transition in its own native measurement language?

The shared schema is:

`state / control / transform / invariant / drift / coherence / score`

The shared scoring intuition remains:

`score = preserved_structure - drift_penalty`

## Claim Boundary

This atlas is a test map.

It does not say that chemistry, genomics, cells, ecology, or infrastructure are
already solved. It says each domain can be converted into a disciplined
comparator surface with:

- a state object
- a control object
- a transform or perturbation
- an invariant / coherence observable
- a drift or disorder mode
- a first safe test

## Nest-Level Map

| Nest | Domain | Role In The Big Paper |
| --- | --- | --- |
| `Nest 1` | formal systems | reductionist base: linear algebra, symmetries, invariants, encoded states |
| `Nest 2` | constrained structured systems | matter-facing structure: elements, molecules, graphs, crystals, materials |
| `Nest 3` | classical coherence systems | resonance / timing bridge: oscillators, fields, spectra, phase-lock |
| `Nest 4` | biological comparator systems | live organization: HRV, EEG, cells, genome regulation, physiology |
| `Nest 5` | multi-class convergence | cross-domain recurrence: same score logic across completed classes |

## Universal Comparator Matrix

| System Class | State Object | Transform / Control | Invariant / Coherence Observable | Drift / Disorder Mode | First Safe Test |
| --- | --- | --- | --- | --- | --- |
| linear algebra | vectors, matrices, subspaces, projections | basis change, projection, perturbation, shuffle | rank, norm, angle, overlap, eigenspectrum, subspace alignment | basis scrambling, projection instability, angle collapse | compare target transforms against shuffled/null transforms |
| symmetry / group structure | permutations, signs, reflections, representations | valid symmetry action vs invalid action | conserved orbit, parity, commutation, subgroup relation | symmetry break, non-commuting rewrite, random permutation | test invariant preservation under valid vs random actions |
| encoded circuit states | statevectors, amplitudes, observables, stabilizer-like signatures | PennyLane / Qiskit encoding, backend run, Bell/control comparison | fidelity, expectation values, parity, Bell/control direction | backend noise, readout drift, feature collapse | repeat encoded feature states across simulator and hardware paths |
| AI hidden states | residual streams, hidden vectors, token-position geometry | packet/control, rerun, localization, readout bridge | separation, late-band structure, anchor stability, bridge carry-through | stochastic drift, localization loss, target/control collapse | use completed `V7` through `Phase 5` rows as reference signature |
| semantic feature states | compressed feature vectors and semantic settings | `A`, `A'`, `B`, `B'` setting choice | bounded output correlations, semantic CHSH-style score | setting leakage, overfit threshold, control violation | locked `Phase 10` semantic contextuality protocol |
| elements / periodic table | atomic number, shell structure, valence, families | family grouping, shuffled family labels, feature embeddings | periodic recurrence, valence class stability, shell relation | family scrambling, false clustering, random alignment | test whether comparator recovers periodic families above shuffled controls |
| molecular families | molecular graphs, stoichiometry, bond topology, functional groups | graph embedding, family shuffle, bond perturbation | conserved topology, subgraph motifs, valence consistency | random graph mismatch, topology distortion, family collapse | classify molecule families and compare against shuffled graph controls |
| `H2O` / water | bond angle, polarity, hydrogen-bond network, phase context | molecular graph, network perturbation, thermal / phase comparison | constrained angle, polarity relation, network coordination | bond-angle distortion, network decoherence, phase disruption | compare water motif against related small molecules and shuffled networks |
| crystals / materials | lattice structure, unit cell, symmetry group, defects | lattice transform, defect insertion, strain perturbation | space-group relation, lattice periodicity, phonon / band structure | defect drift, symmetry loss, strain disorder | test preserved lattice invariants under controlled perturbation |
| reaction networks | reactants, products, pathways, catalysts, kinetics | pathway perturbation, rate change, catalyst/control comparison | stoichiometric balance, conserved mass/charge, pathway stability | runaway path, side reaction, rate instability | compare stable pathway families against random reaction graphs |
| persistent pollutant remediation | `PFAS / PFCs / forever chemicals`, fluorinated compounds, pharmaceuticals, pesticides, industrial organics, microplastics, degradation byproducts, treatment conditions | adsorption, membrane, AOP, ARP, SCWO, plasma, sonolysis, photocatalysis, electrochemical controls | parent reduction, defluorination / mineralization, byproduct suppression, toxicity / bioactivity reduction | partial breakdown, harmful byproducts, transfer to sludge/air, microfragmentation, persistent active metabolites | literature matrix first, then benchtop analogs and partner-lab contaminant tests |
| thermodynamic states | temperature, pressure, entropy, phase, free energy | phase transition, cooling/heating, pressure change | phase boundary, conservation relation, energy minimum | instability, hysteresis, uncontrolled entropy growth | map transition stability and drift across known phase diagrams |
| oscillators | coupled signals, phase, amplitude, frequency | coupling strength, detuning, noise injection | phase-lock, coherence window, entrainment ratio | phase slip, decoherence, broadband noise | compare synchronized vs shuffled oscillator pairs |
| resonance systems | frequency response, amplitude envelope, Q factor | sweep, detuning, damping, control tone | resonance peak, bandwidth, stable mode | peak drift, damping collapse, harmonic noise | score resonance-window preservation under repeat sweeps |
| terahertz cellular resonance | THz frequency / power / timing mapped to cellular, DNA, hydration, and expression states | frequency sweep, off-resonance control, sham, heat-matched control | low-drift target-state movement, methylation / expression module shift, hydration or membrane-state coherence | heat, stress response, DNA damage, off-target expression, artifact | build literature matrix first, then only later partner-run in-vitro protocol |
| `EMF` / spectral fields | bands, phase relations, amplitudes, coupling | frequency sweep, shielding/control, source on/off | spectral clustering, phase stability, coupling signature | phase instability, noise dominance, artifact coupling | compare phase-lock metrics against shielded/null sessions |
| fluid / wave systems | waves, vortices, flow fields, boundary conditions | perturbation, boundary change, forcing | stable mode, vortex persistence, conserved flow relation | turbulence, dispersion, boundary chaos | compare coherent structures under controlled forcing vs random forcing |
| genome sequence | nucleotide sequence, k-mers, motifs, conserved regions | shuffle, mutation model, species/family comparison | motif conservation, GC structure, synteny, repeat architecture | random mutation, motif loss, sequence entropy | compare conserved motifs against shuffled and family-local controls |
| epigenome / chromatin | methylation, histone marks, chromatin loops, accessibility | condition change, cell-type comparison, perturbation | regulatory-region stability, loop domains, accessibility modules | dysregulated marks, loop loss, expression noise | map regulatory modules across cell types with shuffled-region controls |
| transcriptome | gene-expression vectors, modules, time-series states | condition/control, time shift, perturbation | co-expression modules, trajectory stability, pathway coherence | expression noise, module fragmentation, off-target activation | compare expression module preservation under known biological conditions |
| proteome / allostery | protein structures, conformations, interaction networks | ligand binding, mutation, allosteric perturbation | conserved fold, active site relation, conformational pathway | misfolding, binding loss, pathway instability | compare conformational-state transitions against mutation/null controls |
| cellular signaling | membrane potential, calcium pulses, receptor cascades | stimulus/control, inhibition, timing perturbation | pulse timing, threshold stability, pathway coordination | desynchronization, runaway signaling, threshold collapse | score signaling pulse coherence under repeated controlled windows |
| tissue / organ rhythms | cardiac, neural, respiratory, endocrine timing | baseline/condition/post, entrainment, recovery | rhythm stability, coupling, recovery tail, coherence | arrhythmia, desynchronization, poor recovery | extend `HRV` into EEG-HRV and later richer physiology |
| neural dynamics | EEG bands, phase, coherence, event-related windows | task/control, entrainment, rest/post windows | alpha/theta power, phase-lock, cross-band coupling | broadband noise, motion artifact, unstable coupling | run simultaneous `EEG + HRV` with fixed timing windows |
| human-state adapter | HRV/EEG/user feedback vectors | orchestration tuning, pacing change, response mode | state fit, reduced interaction drift, recovery support | overreaction, misread state, context pressure mismatch | test side-channel routing in LSPS before deeper model insertion |
| ecological systems | populations, flows, cycles, niches, network relations | disturbance/control, seasonal comparison, restoration action | network resilience, nutrient cycling, biodiversity structure | collapse, invasive drift, cycle disruption | compare ecosystem network stability under known perturbation datasets |
| infrastructure / grids | nodes, loads, flows, constraints, failure modes | rerouting, outage, demand shift, optimization control | load balance, resilience, constraint satisfaction | cascade failure, overload, unstable routing | apply comparator scoring to grid-planning / resilience simulations |
| supply / logistics networks | inventory, nodes, routes, timing, demand | route change, disruption, demand shock | throughput stability, bottleneck reduction, recovery | queue growth, route collapse, delay cascade | score recovery and load balancing under controlled disruption |
| social / organizational systems | roles, communication flows, decisions, feedback loops | process change, routing, coordination structure | alignment, stable handoff, reduced rework, signal clarity | fragmentation, bottleneck, trust drift, loop failure | use only aggregate/non-sensitive process metrics and controls |
| AI orchestration systems | agents, tools, routes, verification checks, memory | routing policy, verifier change, context compression | continuity, tool success, verification stability, reduced drift | context collapse, wrong tool use, runaway loop | use Mirror / LSPS session-state metrics as direct engineering lane |

## Genome-Specific Pattern Overlay

The genome lane is important because it gives a way to test pattern recurrence
inside biological information structure without immediately making clinical
claims.

### Candidate State Objects

- raw DNA sequence
- k-mer frequency structure
- conserved motifs
- regulatory regions
- chromatin accessibility regions
- methylation / histone marks
- gene-expression modules
- 3D chromatin contact maps

### Candidate Controls

- shuffled sequences preserving base composition
- shuffled genomic intervals
- family-local controls
- random motif placements
- matched-length non-regulatory regions
- time-shifted expression controls

### Candidate Invariants

- motif conservation
- GC / k-mer structure
- synteny blocks
- regulatory module preservation
- co-expression modules
- chromatin domain stability
- pathway-level expression coherence

### Candidate Drift Modes

- motif loss
- expression noise
- regulatory module fragmentation
- chromatin-loop disruption
- mutation burden
- off-target pathway activation

### First Safe Test

Use public non-clinical genomic datasets and ask:

Can the Mirror comparator recover conserved motif / regulatory / expression
module structure better than shuffled or matched null controls?

This keeps the genome lane as a structure-and-information test first, not a
clinical claim.

## Chemical And Materials Pattern Overlay

Chemistry should be treated as constrained relational structure.

The first chemistry question is not whether a molecule "is the mirror." The
first question is whether the same comparator logic can recover:

- family structure
- valence constraints
- bond topology
- geometric regularity
- conserved composition
- stable reaction paths

Best first targets:

1. periodic-table family recovery
2. simple molecular-family clustering
3. `H2O` relational geometry
4. small reaction-network conservation
5. crystal / material lattice invariants

Controls:

- shuffled element labels
- shuffled bond graphs
- matched composition but broken topology
- random graph baselines
- perturbed lattice / defect controls

## Biological Pattern Overlay Beyond HRV

`Phase 12B` proves the live `HRV` adapter lane exists. The broader biological
map should grow outward from that anchor.

Next biological layers:

- simultaneous `EEG + HRV`
- respiratory timing
- sleep / recovery timing if instrumented cleanly
- cellular calcium timing
- membrane-potential / excitability comparators
- gene-expression time series
- protein / receptor conformational transitions
- tissue rhythm synchronization

The safe rule:

Each biological layer must have its own measurement surface and controls. The
architecture can carry the score logic, but the biology must carry its own
evidence.

## Terahertz Cellular Resonance Overlay

The terahertz lane is a special `Nest 3 -> Nest 4` bridge:

- `Nest 3` supplies frequency, resonance, spectral exposure, and phase /
  timing structure
- `Nest 4` supplies cell state, DNA methylation, gene expression, hydration,
  membrane state, calcium signaling, and later physiological readouts

Dedicated bridge note:

- [Terahertz Cellular Resonance Bridge](./TERAHERTZ_CELLULAR_RESONANCE_BRIDGE_2026-04-24.md)
- [Terahertz Chemical Remediation Bridge](./TERAHERTZ_CHEMICAL_REMEDIATION_BRIDGE_2026-04-24.md)

The first question is not whether terahertz is healing. The first question is:

Can a terahertz exposure pattern be scored as moving a biological state toward
a target class while avoiding heat, stress, DNA damage, expression noise, and
artifact penalties?

## Persistent Pollutant Remediation Overlay

The far-future environmental lane maps terahertz and Mirror Architecture into
chemical remediation without pretending spectroscopy alone destroys difficult
pollutants.

Target classes:

- `PFAS` as the umbrella term
- older `PFC` terminology
- "forever chemicals"
- fluorinated compounds
- named examples such as `PFOA`, `PFOS`, `PFHxS`, and `GenX`
- pharmaceuticals and active metabolites
- pesticides / herbicides
- persistent industrial organics
- persistent industrial chemicals
- microplastics / nanoplastics
- contaminated water, soil, sludge, and residual streams

The clean process chain is:

identify -> separate / concentrate -> activate / degrade / destroy -> verify
non-toxic or lower-risk byproducts -> prevent transfer into another medium

The Mirror role is the optimization layer:

- map the contaminant chain
- map the molecular bond graph
- map likely degradation pathways
- identify target bonds for cleavage
- score parent reduction
- score defluorination / mineralization where relevant
- penalize harmful byproducts
- verify mineralization / defluorination when relevant
- minimize energy and transfer risk

The first safe test is a literature and public-data matrix, not field exposure.

For `PFAS`, parent-compound disappearance is not enough. The target is
bond-level verification:

- carbon-fluorine bond cleavage
- free fluoride recovery
- suppression of short-chain PFAS descendants
- byproduct identification
- toxicity reduction
- mass-balance closure

## Multi-Class Convergence Rule

The project gets stronger when the same comparator spine works across many
classes:

- formal
- encoded
- hardware
- chemical
- material
- genomic
- cellular
- physiological
- coherence / spectral
- ecological
- engineered systems

The final convergence claim should not depend on one dramatic hit. It should
come from repeated class-level recurrence:

same score logic, different substrates, matched controls, repeatable
separation.

## First Build Order From This Atlas

1. finish `Nest 1` synthesis from the existing formal matrix
2. create `Nest 2A` periodic-table / element-family comparator
3. create `Nest 2B` molecular graph / `H2O` comparator
4. create `Nest 3A` oscillator / resonance comparator
5. create `Nest 3B` spectral / phase-lock comparator
6. prepare `Nest 4A` simultaneous `EEG + HRV`
7. prepare `Nest 4B` genome / expression-module design note
8. run `ARC15` fixed-layout physical-control sessions
9. build `Phase 12C` synchronized overlay
10. merge completed rows into `Nest 5` convergence matrix

## Short Read

This is the atlas for the big paper.

The theory may eventually touch many systems, but the method stays grounded:
define the state, define the control, define the transform, define the
invariant, measure drift, score preserved structure, and only strengthen the
claim when multiple substrates show recurring alignment.
