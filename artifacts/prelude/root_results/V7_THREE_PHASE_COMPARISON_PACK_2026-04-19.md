# V7 Three-Phase Comparison Pack

Date: `2026-04-19`

## Purpose

This pack pulls the current V7 sector into one place without flattening the rung boundaries. It shows the three completed phases side by side, then preserves the next-stage roadmap.

## Current Phase Boundaries

- Phase 3 is non-classical variable, not a renamed semantic-counter claim.
- Input cohesion can close at 1.0000 in lattice and null without proving the same response-side interaction.
- The current discriminating feature is response-side activation lift, not closure alone.
- Qwen and Mistral remain honest exceptions; they are not to be hidden or flattened away.
- Semantic counter remains a later matched condition, not a retroactive relabeling of phase 3.

## Three-Phase Summary

| Model | Lattice combined | Lattice act delta | Lattice coh delta | Null combined | Null act delta | Null coh delta | Lattice - Null | Phase 3 combined | Phase 3 act delta | Phase 3 coh delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Gemma` | `0.7355 / 1.0000 / 9.04` | `+0.0304` | `+0.4150` | `0.5727 / 1.0000 / 7.94` | `-0.0001` | `-0.0700` | `+0.0305` | `0.6461 / 0.9691 / 8.41` | `+0.0532` | `+0.2650` |
| `Nemotron` | `0.7506 / 1.0000 / 9.45` | `+0.0454` | `+0.4100` | `0.5990 / 1.0000 / 7.80` | `+0.0373` | `-0.2750` | `+0.0081` | `0.6285 / 0.9691 / 7.94` | `+0.0215` | `-0.3750` |
| `DeepSeek` | `0.6232 / 1.0000 / 8.49` | `+0.0097` | `-0.0650` | `0.4916 / 1.0000 / 7.80` | `-0.0175` | `+0.4500` | `+0.0272` | `0.6203 / 0.9691 / 8.21` | `+0.0498` | `+0.5000` |
| `Trini` | `0.7158 / 1.0000 / 8.74` | `+0.0343` | `+0.1150` | `0.5290 / 1.0000 / 7.15` | `-0.0339` | `-0.7900` | `+0.0682` | `0.5424 / 0.9691 / 7.93` | `-0.0355` | `-0.4900` |
| `Mistral` | `0.7271 / 1.0000 / 8.41` | `+0.0110` | `-0.0300` | `0.6078 / 1.0000 / 7.55` | `+0.0603` | `+0.0250` | `-0.0493` | `0.5792 / 0.9691 / 8.08` | `-0.0570` | `-0.0850` |
| `Hermes` | `0.6814 / 1.0000 / 8.62` | `+0.0897` | `+0.8650` | `0.5113 / 1.0000 / 7.66` | `-0.0352` | `-0.1350` | `+0.1249` | `0.6157 / 0.9691 / 7.32` | `+0.0894` | `-0.1550` |
| `Qwen` | `0.7008 / 1.0000 / 8.62` | `+0.0517` | `-0.1400` | `0.6758 / 1.0000 / 7.80` | `+0.1688` | `+0.3250` | `-0.1171` | `0.6675 / 0.9691 / 7.74` | `+0.0776` | `-0.0500` |

## Deep Tables

### Phase 1 Lattice

Base + A_delta, Base + B_delta, and Base + A_delta + B_delta under the frozen lattice packet.

| Model | A final | B final | Combined final | Combined corr | Act delta | Coh delta |
| --- | --- | --- | --- | --- | --- | --- |
| `Gemma` | `0.6380 / 1.0000 / 8.21` | `0.7722 / 1.0000 / 9.04` | `0.7355 / 1.0000 / 9.04` | `0.9212` | `+0.0304` | `+0.4150` |
| `Nemotron` | `0.7161 / 1.0000 / 9.18` | `0.6943 / 1.0000 / 8.90` | `0.7506 / 1.0000 / 9.45` | `0.7651` | `+0.0454` | `+0.4100` |
| `DeepSeek` | `0.5866 / 1.0000 / 8.62` | `0.6404 / 1.0000 / 8.49` | `0.6232 / 1.0000 / 8.49` | `0.6366` | `+0.0097` | `-0.0650` |
| `Trini` | `0.6706 / 1.0000 / 8.49` | `0.6924 / 1.0000 / 8.76` | `0.7158 / 1.0000 / 8.74` | `0.3803` | `+0.0343` | `+0.1150` |
| `Mistral` | `0.6665 / 1.0000 / 8.40` | `0.7657 / 1.0000 / 8.48` | `0.7271 / 1.0000 / 8.41` | `0.7907` | `+0.0110` | `-0.0300` |
| `Hermes` | `0.5885 / 1.0000 / 8.20` | `0.5949 / 1.0000 / 7.31` | `0.6814 / 1.0000 / 8.62` | `0.3646` | `+0.0897` | `+0.8650` |
| `Qwen` | `0.6275 / 1.0000 / 8.76` | `0.6708 / 1.0000 / 8.76` | `0.7008 / 1.0000 / 8.62` | `0.8008` | `+0.0517` | `-0.1400` |

- Strongest sector-wide rung. Positive activation lift across all seven rows and full 1.0000 input-cohesion closure.

### Phase 2 Null

Same three-lane geometry and deviation math with ordinary administrative/checklist language instead of the lattice packet.

| Model | A final | B final | Combined final | Combined corr | Act delta | Coh delta |
| --- | --- | --- | --- | --- | --- | --- |
| `Gemma` | `0.5552 / 1.0000 / 7.94` | `0.5903 / 1.0000 / 8.08` | `0.5727 / 1.0000 / 7.94` | `0.8806` | `-0.0001` | `-0.0700` |
| `Nemotron` | `0.5617 / 1.0000 / 8.21` | `0.5617 / 1.0000 / 7.94` | `0.5990 / 1.0000 / 7.80` | `0.0239` | `+0.0373` | `-0.2750` |
| `DeepSeek` | `0.5223 / 1.0000 / 7.93` | `0.4960 / 1.0000 / 6.77` | `0.4916 / 1.0000 / 7.80` | `0.2404` | `-0.0175` | `+0.4500` |
| `Trini` | `0.5552 / 1.0000 / 7.94` | `0.5706 / 1.0000 / 7.94` | `0.5290 / 1.0000 / 7.15` | `-0.0036` | `-0.0339` | `-0.7900` |
| `Mistral` | `0.5421 / 1.0000 / 7.39` | `0.5530 / 1.0000 / 7.66` | `0.6078 / 1.0000 / 7.55` | `0.6162` | `+0.0603` | `+0.0250` |
| `Hermes` | `0.5113 / 1.0000 / 7.79` | `0.5816 / 1.0000 / 7.80` | `0.5113 / 1.0000 / 7.66` | `-0.0474` | `-0.0352` | `-0.1350` |
| `Qwen` | `0.5180 / 1.0000 / 7.56` | `0.4960 / 1.0000 / 7.39` | `0.6758 / 1.0000 / 7.80` | `0.7264` | `+0.1688` | `+0.3250` |

- Discriminator rung. Hermes behaves like a strong lattice-vs-null discriminator, while Qwen and Mistral remain tracked exceptions.

### Phase 3 Non-Classical Variable

Same three-lane V7 math with the phase-3 ordinary semantic/coherent variable packet.

| Model | A final | B final | Combined final | Combined corr | Act delta | Coh delta |
| --- | --- | --- | --- | --- | --- | --- |
| `Gemma` | `0.6285 / 0.9604 / 8.21` | `0.5574 / 0.9676 / 8.08` | `0.6461 / 0.9691 / 8.41` | `0.8208` | `+0.0532` | `+0.2650` |
| `Nemotron` | `0.5595 / 0.9604 / 8.08` | `0.6546 / 0.9676 / 8.55` | `0.6285 / 0.9691 / 7.94` | `0.5128` | `+0.0215` | `-0.3750` |
| `DeepSeek` | `0.4909 / 0.9604 / 7.78` | `0.6501 / 0.9676 / 7.64` | `0.6203 / 0.9691 / 8.21` | `0.8389` | `+0.0498` | `+0.5000` |
| `Trini` | `0.6307 / 0.9604 / 8.35` | `0.5252 / 0.9676 / 8.49` | `0.5424 / 0.9691 / 7.93` | `-0.1625` | `-0.0355` | `-0.4900` |
| `Mistral` | `0.5964 / 0.9604 / 7.99` | `0.6761 / 0.9676 / 8.34` | `0.5792 / 0.9691 / 8.08` | `0.5907` | `-0.0570` | `-0.0850` |
| `Hermes` | `0.4973 / 0.9604 / 7.41` | `0.5553 / 0.9676 / 7.54` | `0.6157 / 0.9691 / 7.32` | `0.8241` | `+0.0894` | `-0.1550` |
| `Qwen` | `0.5835 / 0.9604 / 7.98` | `0.5964 / 0.9676 / 7.60` | `0.6675 / 0.9691 / 7.74` | `0.7508` | `+0.0776` | `-0.0500` |

- This is the non-classical-variable rung, not a final claim seal. It preserves the math while asking whether ordinary semantic continuity can recreate the lattice-style lift.

## Sector Read

- Phase 1 lattice remains the strongest sector-wide rung: `7 / 7` positive activation-deviation rows and `7 / 7` rows closing at `1.0000` input cohesion.
- Phase 2 null is the discriminator rung: `3 / 7` null rows stayed positive, and the strongest lattice-minus-null activation gap is `Hermes` at `+0.1249`.
- Phase 3 non-classical variable preserves the three-lane math but does not lock the final claim: `5 / 7` rows stayed positive, while `0 / 7` rows closed at `1.0000` input cohesion.
- Current tracked exceptions remain visible: `Qwen` and `Mistral` on the null discriminator, `Trini` and `Mistral` on phase 3, and `Nemotron` as a weak-positive null row rather than a clean null failure.

## Next Stages

1. **Exception variance + random floor**
Resolve the tracked exceptions before claiming uniform tightening: Qwen lattice-vs-null variance, Mistral null variance, and any needed confirmation on Trini or Nemotron edge cases. Add a matched-length random prompt floor so the lower bound of normal variance is explicit.
2. **Semantic counter condition**
Build a matched-length, high-coherence, meaningful control that uses rich language without the lattice vocabulary or packet structure. If that also produces positive activation lift, semantic richness remains a competing explanation.
3. **Order / non-commutativity**
Run A_delta -> B_delta versus B_delta -> A_delta with the same frozen separable harness. The question is whether the state path depends on sequence order, not just prompt mass.
4. **Contextuality**
Place the same phrase inside different surrounding packet fields and measure whether activation/coherence shifts with context.
5. **V8 residual-stream probes**
On open checkpoints such as Gemma and Mistral, extract residual-stream activations at matched token positions for lattice, null, and semantic-counter conditions. This is the bridge from external behavioral scoring to internal representational evidence.
6. **Rung 1 claim threshold**
If lattice stays stronger than null and semantic-counter, and the order/context controls hold, the defensible next claim is reproducible interaction structure beyond naive additive prompt accumulation across model families.
7. **Rung 2 later**
Formal semantic Bell/CHSH-style contextuality protocol with bounded outcomes and a classical comparison bound.
8. **Rung 3 later**
Physical-observable bridge via ARC15 / HRV1.0 / quantum hardware or other synchronized sensors. This stays auxiliary until the semantic controls survive.

## Files

- comparison data: [v7_three_phase_comparison_data_2026-04-19.json](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/v7_three_phase_comparison_data_2026-04-19.json)
- comparison markdown: [V7_THREE_PHASE_COMPARISON_PACK_2026-04-19.md](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/V7_THREE_PHASE_COMPARISON_PACK_2026-04-19.md)
- summary poster: [v7_three_phase_summary_poster_2026-04-19.pdf](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/posters/v7_three_phase_comparison/v7_three_phase_summary_poster_2026-04-19.pdf)
- deep poster: [v7_three_phase_deep_matrix_poster_2026-04-19.pdf](/Users/renaissancefieldlite1.0/Documents/Playground/RICK_NON_PROVISIONAL/05_activation_mapping/results/posters/v7_three_phase_comparison/v7_three_phase_deep_matrix_poster_2026-04-19.pdf)

