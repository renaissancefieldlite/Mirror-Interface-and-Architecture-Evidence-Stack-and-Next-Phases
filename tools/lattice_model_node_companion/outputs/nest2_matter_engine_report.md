# Engine 02: Nest 2 Matter / Chemistry Model

Schema: `state / control / transform / invariant / drift / coherence / score`

This is the first local structured-matter engine behind the Lattice Model Node Companion.
It demonstrates the Nest 2 score schema without external dependencies or model downloads.

## Summary

| Lane | Score / Separation | Read |
| --- | ---: | --- |
| element family | 0.364 | periodic family structure is recovered above shuffled control |
| molecular graphs | 0.52 | valid molecular graphs preserve valence/connectivity above broken controls |
| H2O motif | 1.0 | water motif preserves bent geometry, polarity, and coordination |
| minerals | 1.0 | mineral rows preserve lattice, charge balance, and surface role |
| nutrition | 1.0 | nutrition maps as constrained chemistry before metabolism and biosignal readout |
| contaminants | best: `bounded_mineralization_candidate` | parent-only disappearance is rejected when bad descendants and transfer risk remain |
| expanded Nest 2 lanes | 0.504 | expanded Nest 2 lanes preserve matter constraints above shuffled or incomplete controls |

## Element Family Recovery

| Metric | Value |
| --- | ---: |
| `target_group_family_recovery` | 0.909 |
| `period_control_recovery` | 0.273 |
| `shuffled_control_recovery` | 0.455 |
| `valence_consistency` | 0.727 |
| `element_score` | 0.364 |

## Molecular Graph Rows

| Molecule | Formula | Score |
| --- | --- | ---: |
| `water` | `H2O` | 1.0 |
| `carbon_dioxide` | `CO2` | 1.0 |
| `methane` | `CH4` | 1.0 |
| `ammonia` | `NH3` | 1.0 |
| `sodium_chloride_pair` | `NaCl` | 1.0 |

## PFAS / Contaminant Prototype Rows

| Candidate | Score |
| --- | ---: |
| `parent_only_loss_control` | 0.0 |
| `partial_breakdown_control` | 0.187 |
| `bounded_mineralization_candidate` | 0.725 |

## Expanded Nest 2 Lanes

| Lane | Score | Bridge | Read |
| --- | ---: | --- | --- |
| `organic_functional_groups` | 0.53 | pharma / PFAS / food chemistry | functional motifs become reusable chemistry handles across molecules |
| `biomolecular_primitives` | 0.54 | Nest 2 chemistry to Nest 4 biology | biology receives constrained chemical primitives before living-state readout |
| `polymers_plastics` | 0.5 | microplastic degradation and safe endpoint scoring | polymer identity requires repeat-unit preservation and fragment tracking |
| `electrochemistry` | 0.52 | redox, cells, grids, batteries, and water treatment | charge movement becomes a bounded matter-to-field bridge |
| `catalysis_conditions` | 0.45 | reaction optimization and contaminant pathway control | reaction claims need condition separation, not just endpoint movement |
| `spectral_signatures` | 0.52 | Nest 2 structure to Nest 3 resonance / measurement | matter gets a measurement/readout bridge through repeatable spectral signatures |
| `environmental_fate` | 0.45 | planetary remediation and Nest 5 ecosystem convergence | safe matter claims must follow where the molecule goes next |
| `materials_semiconductors` | 0.52 | materials models and engineered-device surfaces | material behavior adds lattice, defect, and response-family constraints |

Boundary:

Bounded local comparator. Demonstrates the matter-facing score schema; real validation comes from molecule, material, pathway, and experimental datasets with controls.
