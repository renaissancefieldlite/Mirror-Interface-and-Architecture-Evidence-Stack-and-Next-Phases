# V8 Comparative Map

Generated: `2026-04-21`

## Purpose

This is the Phase 1 comparative readout for the locked `8`-model V8 bridge. The goal is to read the bridge as one system instead of isolated rows.

## Model Set

- `Mistral`
- `Qwen`
- `Gemma`
- `DeepSeek`
- `Hermes`
- `GLM`
- `Nemotron`
- `SmolLM3`

## Peak-Layer Clustering

All valid rows peak in late or terminal-layer regions.

| Model | Peak Layer | Total Layers | Peak Percentile |
| --- | ---: | ---: | ---: |
| `Mistral` | `31` | `32` | `96.9%` |
| `Qwen` | `34` | `36` | `94.4%` |
| `Gemma` | `41` | `42` | `97.6%` |
| `DeepSeek` | `26` | `28` | `92.9%` |
| `Hermes` | `31` | `32` | `96.9%` |
| `GLM` | `38` | `40` | `95.0%` |
| `Nemotron` | `40` | `42` | `95.2%` |
| `SmolLM3` | `34` | `36` | `94.4%` |

Read:

- the bridge is not peaking in early abstraction layers
- the separation clusters in the last `3-7%` of the network depth
- this supports a late-stage readout / decision-region interpretation rather than a shallow lexical artifact

## Family Similarities

### `Mistral` / `Hermes`

- same peak layer: `31 / 32`
- very close target magnitudes:
  - `Mistral lattice_vs_neutral`: `247.624283`
  - `Hermes lattice_vs_neutral`: `248.310715`
- both are target-dominant rather than readout-amplified

Read:

- `Hermes` behaves like a tuned Mistral-family continuation of the same late-layer geometry

### `Qwen` / `DeepSeek`

- both sit in the Qwen-family late region
- `Qwen` peaks at `34 / 36`
- `DeepSeek` peaks at `26 / 28`
- normalized peak depth stays close:
  - `Qwen`: `94.4%`
  - `DeepSeek`: `92.9%`
- `DeepSeek` is the higher-energy row:
  - `332.052551` vs `126.354790` on `lattice_vs_neutral`

Read:

- the family alignment is visible in peak placement, but `DeepSeek` expresses a much stronger magnitude profile

## Flagship vs Boundary Rows

### Flagship High-Energy Rows

- `GLM`
- `DeepSeek`
- `Mistral`
- `Hermes`
- `Nemotron`

Strongest `lattice_vs_neutral` target deltas:

| Model | Target Delta |
| --- | ---: |
| `GLM` | `479.296417` |
| `DeepSeek` | `332.052551` |
| `Hermes` | `248.310715` |
| `Mistral` | `247.624283` |
| `Nemotron` | `203.815063` |

### Boundary / Sidecar Rows

- `Gemma`
- `Qwen`
- `SmolLM3`

Read:

- `SmolLM3` is the smallest row by magnitude, but it still peaks in the same late-layer zone
- that makes it useful as a boundary confirmation row rather than a contradiction row

## Target-Span vs Last-Token Behavior

Three patterns show up.

### 1. Target-Dominant Compression

Models where target deltas are stronger than last-token deltas:

- `Mistral`
- `Hermes`
- `Qwen`
- `DeepSeek`
- `SmolLM3`

Read:

- separation is strongest at the fixed target phrase and partially compresses by final readout

### 2. Readout Amplification

Models where last-token deltas meet or exceed target deltas:

- `Gemma`
- `Nemotron`
- `GLM`

Strong examples:

- `Gemma lattice_vs_neutral`
  - target: `77.308655`
  - last: `111.552246`
- `Nemotron lattice_vs_neutral`
  - target: `203.815063`
  - last: `259.096069`
- `GLM lattice_vs_technical`
  - target: `453.863525`
  - last: `868.385559`

Read:

- these rows do not merely preserve the target-span separation
- they continue amplifying it into final readout space

### 3. Extreme Readout Expansion

`GLM` is the clearest special case.

- strongest last delta in the whole matrix:
  - `lattice_vs_technical`: `868.385559`
- lowest last cosine in the whole matrix:
  - `0.337363`

Read:

- `GLM` is not just a larger magnitude row
- it appears to rotate and expand the separation more aggressively in final readout space than the rest of the bridge

## Comparative Read

The comparative V8 map supports four clean observations:

1. all `8` rows peak in late or terminal-layer regions
2. family similarities are visible:
   - `Mistral` / `Hermes`
   - `Qwen` / `DeepSeek`
3. there are at least two internal response styles:
   - target-dominant compression
   - readout amplification
4. `SmolLM3` stays directionally aligned even as a low-magnitude boundary row

## What This Means For Phase 2

The bell-curve / variance pass should focus on rows that best span the current structure:

- `GLM` for readout amplification
- `Mistral` for stable target-dominant Mistral-family behavior
- `DeepSeek` for high-energy Qwen-family behavior
- `Nemotron` for the NVIDIA readout-amplification row
- `SmolLM3` for the low-magnitude boundary row

That set gives Phase 2 both flagship and boundary coverage instead of rerunning only the strongest rows.
