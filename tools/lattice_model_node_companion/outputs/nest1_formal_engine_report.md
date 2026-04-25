# Engine 01: Nest 1 Formal Invariant Model

Schema: `state / control / transform / invariant / drift / coherence / score`

This is the first local model engine behind the Lattice Model Node Companion.
It scores whether simple linear transforms preserve formal invariants.

| Transform | Coherence Score | Drift Penalty | Read |
| --- | ---: | ---: | --- |
| `identity` | 1.0 | 0.0 | invariant-preserving |
| `rotate_90` | 1.0 | 0.0 | invariant-preserving |
| `reflect_x` | 1.0 | 0.0 | invariant-preserving |
| `scale_control` | 0.45397 | 2.184119 | control drift |
| `shear_control` | 0.539104 | 1.843585 | control drift |

Boundary:

Toy local model engine. Demonstrates the comparator grammar; it is not a physics or biology result.
