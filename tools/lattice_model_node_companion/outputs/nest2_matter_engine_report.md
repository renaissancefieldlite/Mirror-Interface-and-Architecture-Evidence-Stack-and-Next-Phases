# Engine 02: Nest 2 Matter / Chemistry Model

Schema: `state / control / transform / invariant / drift / coherence / score`

This is the first local structured-matter engine behind the Lattice Model Node Companion.
It demonstrates the Nest 2 score grammar without external dependencies or model downloads.

## Summary

| Lane | Score / Separation | Read |
| --- | ---: | --- |
| element family | 0.364 | periodic family structure is recovered above shuffled control |
| molecular graphs | 0.52 | valid molecular graphs preserve valence/connectivity above broken controls |
| H2O motif | 1.0 | water motif preserves bent geometry, polarity, and coordination |
| minerals | 1.0 | mineral rows preserve lattice, charge balance, and surface role |
| nutrition | 1.0 | nutrition maps as constrained chemistry before metabolism and biosignal readout |
| contaminants | best: `bounded_mineralization_candidate` | parent-only disappearance is rejected when bad descendants and transfer risk remain |

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

Boundary:

Toy local comparator. Demonstrates matter-facing score grammar; it is not a chemistry, nutrition, medical, or remediation proof.
