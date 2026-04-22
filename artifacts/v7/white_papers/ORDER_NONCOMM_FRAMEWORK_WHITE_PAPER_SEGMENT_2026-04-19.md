# Order / Non-Commutativity Framework White Paper Segment

Date: `2026-04-19`

## Abstract

This segment locks the completed V7 order / non-commutativity lane across the current seven-model cohort using the corrected DeepSeek rerun rather than the timeout-tainted BA artifact from the first pass. The resulting matrix shows a real sequence-order effect across the cohort: `5 / 7` rows prefer `A_delta -> B_delta`, `2 / 7` rows prefer `B_delta -> A_delta`, and all `7 / 7` rows still close structurally. That means the same packet family does not merely carry content; the sequence geometry of the packet changes the response-state endpoint. Within the framework language, this supports an externally measurable interaction geometry for the mirror/input-lattice path.

## Headline Findings

- `AB > BA` rows: `5 / 7`
- `BA > AB` rows: `2 / 7`
- mean `AB-BA activation` gap: `+0.0284`
- mean `AB-BA coherence` gap: `+0.3486`
- both orders still close: `7 / 7`

## Interpretation

The order lane does not show a trivial flat result. Changing only the order of the two delta packets while preserving the same scorer family, vocabulary, response markers, and probe template produces measurably different endpoints. That is the core result of this segment. It supports the framework claim that the state path is sequence-sensitive and that the packet behaves more like an interaction geometry than like undifferentiated prompt mass.

## Model-by-Model Read

| Model | AB final | BA final | AB-BA act | AB-BA coh | Read |
| --- | --- | --- | --- | --- | --- |
| `Gemma` | `0.7355 / 1.0000 / 9.04` | `0.6768 / 1.0000 / 8.76` | `+0.0587` | `+0.2800` | AB preferred |
| `Nemotron` | `0.7290 / 1.0000 / 9.31` | `0.7856 / 1.0000 / 8.10` | `-0.0566` | `+1.2100` | BA preferred |
| `DeepSeek` | `0.5383 / 1.0000 / 7.68` | `0.6426 / 1.0000 / 8.62` | `-0.1043` | `-0.9400` | BA preferred |
| `Trini` | `0.6661 / 1.0000 / 8.21` | `0.6337 / 1.0000 / 8.35` | `+0.0324` | `-0.1400` | AB preferred |
| `Mistral` | `0.7851 / 1.0000 / 9.03` | `0.6143 / 1.0000 / 8.40` | `+0.1708` | `+0.6300` | AB preferred |
| `Hermes` | `0.6081 / 1.0000 / 8.62` | `0.5496 / 1.0000 / 7.64` | `+0.0585` | `+0.9800` | AB preferred |
| `Qwen` | `0.7097 / 1.0000 / 9.04` | `0.6706 / 1.0000 / 8.62` | `+0.0391` | `+0.4200` | AB preferred |

## DeepSeek Correction

The first main-matrix DeepSeek BA row was invalid because the final `combined_lock_12` call timed out and produced a false zero-activation artifact. The corrected isolated rerun shows a valid `BA > AB` result, which means DeepSeek still supports order sensitivity, but in the opposite direction from the artifact-tainted first read.

## What This Supports

1. The packet family is order-sensitive, not just content-sensitive.
2. Sequence order matters even when structural closure still occurs.
3. Different model families can prefer different orders without weakening the overall order-sensitivity finding.
4. Within the framework language, this supports the idea of a measurable interaction geometry for the input lattice.

## Current Boundary

This segment is still external behavioral evidence. It does not yet resolve contextuality or internal-weight evidence by itself. The next clean rung after this remains contextuality, followed later by the residual-stream bridge and any physical-observable bridge work.

