# Next Phase Research Plan From Phase 8

Date: `2026-04-22`

## Current Locked State

The evidence stack is now locked through `Phase 8`.

Current ladder:

1. `V7` - behavioral lattice/control separation
2. `V8` - late-layer internal hidden-state separation
3. `Phase 2` - rerun / variance lock
4. `Phase 3` - dimension and late-band structure
5. `Phase 4` - token-path localization and localization variance
6. `Phase 5` - context-to-readout bridge map
7. `Phase 6` - `PennyLane` quantum-bridge encoding discovery
8. `Phase 7` - `Qiskit` mirror / simulator lock
9. `Phase 8` - Bell-state calibration

Current best read:

- the Mirror Interface / lattice architecture produces measurable behavioral
  and internal hidden-state separation
- the effect repeats under variance discipline
- the effect localizes along the token path and bridges from context toward
  readout
- the locked geometry can be encoded into circuit state spaces
- the `PennyLane` encoding mirrors cleanly in `Qiskit`
- the Bell-state observable path is calibrated on a known `|Phi+>` state

The next plan starts from that base.

## Strategic Meaning Of Phase 6-8

`Phase 6-8` shift the work from only "AI model evidence" into a quantum-bridge
program.

They create:

- AI-feature encoded circuit states
- cross-framework simulator agreement
- a calibrated Bell-state observable/scoring path
- a concrete path toward noisy simulation, hardware/backend tests, and later
  Bell-type semantic contextuality

This is why the support need is now more explicit:

- funding creates the operating room to keep building and researching
- compute expands reruns, model matrices, encoding sweeps, Qiskit/noisy
  simulation, and hardware preparation
- strategic support opens applied problem surfaces, cloud/quantum
  infrastructure, and partner validation paths

## Phase 9 - Bell-Type Semantic Contextuality Protocol

### Objective

Turn the descriptive contextuality and bridge evidence into a formal
Bell-type semantic contextuality protocol.

This is the next real claim-bearing rung.

### Core Question

Do semantic measurement settings built from the Mirror Interface / lattice
architecture produce bounded outcome correlations that exceed a classical
contextual baseline?

### Important Boundary

This is not the same as `Phase 8`.

- `Phase 8` calibrated a known quantum Bell state.
- `Phase 9` tests whether semantic / AI-side settings produce a formal
  contextuality-style result.

### Candidate Measurement Settings

The protocol needs four settings:

- `A` - lattice / mirror-coherence context
- `A'` - matched non-lattice context, likely neutral or technical
- `B` - target-span measurement
- `B'` - readout / last-token / alternate-position measurement

Alternative setting map to compare:

- `A` - lattice packet
- `A'` - semantic-counter packet
- `B` - original order
- `B'` - order-reversed / order-permuted packet

The first design should be conservative:

- use settings already supported by `V7`, `V8`, and `Phase 4-5`
- avoid inventing a new prompt family before the baseline protocol is locked
- keep all outcomes bounded and pre-registered

### Bounded Outcome Candidates

Each trial needs a bounded output, usually `+1` or `-1`.

Candidate outcome definitions:

- sign of normalized lattice/control separation above a fixed threshold
- sign of target-span delta relative to matched neutral/technical control
- sign of readout carry-through ratio relative to pre-registered baseline
- binary classifier from public-safe summary features, not raw private scanner
  internals

Preferred first outcome:

- project the response-state feature vector onto the locked `Phase 3-5`
  direction
- return `+1` if it exceeds the pre-registered threshold
- return `-1` otherwise

Reason:

- it uses the existing measured geometry
- it avoids loose qualitative scoring
- it can be mirrored into the Qiskit feature-state pipeline

### Model Matrix

First focused subset:

- `Mistral`
- `Hermes`
- `Gemma`
- `GLM`
- `Nemotron`
- `SmolLM3`

Reason:

- `Mistral / Hermes` are the cleanest late-context bridge pair
- `Gemma` is the clearest readout-led row
- `GLM` and `Nemotron` are bridge rows
- `SmolLM3` is the diffuse boundary row

Expansion set:

- `Qwen`
- `DeepSeek`

Reason:

- they preserve the front-context family lane
- `DeepSeek` is strong but can dominate magnitude, so it is better after the
  first protocol is stable

### Run Discipline

Minimum:

- `5` reruns per setting pair
- exact config manifest
- fixed prompt packet
- fixed token-position windows
- fixed outcome threshold
- separate result JSON per run

Preferred:

- `10` reruns for final claim table if compute allows
- bootstrap confidence intervals
- control-ladder comparison against null/random/technical/semantic-counter

### Classical Comparison

Compute a CHSH-style score:

`S = E(A,B) + E(A,B') + E(A',B) - E(A',B')`

Interpretation ladder:

- `S <= 2`: no Bell-type exceedance
- `S > 2`: candidate semantic contextuality signal
- `S` near `2*sqrt(2)`: strong result, but requires serious audit

Important:

- semantic contextuality is not physical Bell nonlocality
- it must be described as semantic / AI-side contextuality unless a later
  physical bridge is built

### Artifacts

Public-safe outputs:

- protocol spec
- setting map
- bounded-outcome definition
- model/run manifest
- CHSH-style score table
- control comparison table
- confidence / variance plots
- interpretation note

Private outputs:

- backend scanner code
- mapper internals
- orchestration code
- transformer-runner implementation

### Success Condition

Phase 9 is successful if:

- all settings are pre-registered
- outcomes are bounded
- controls are included
- the score is reproducible under rerun discipline
- the interpretation stays within semantic contextuality boundaries

## Phase 10 - Noisy Simulation And Hardware-Ready Qiskit Path

### Objective

Move the Phase 7 / Phase 8 circuits from ideal statevector simulation toward
hardware-ready testing.

### Core Question

Do the encoded AI-feature states and Bell calibration states survive under
shot-based sampling, noise models, and eventually hardware/backend execution?

### Inputs

- `Phase 6` encoded feature vectors
- `Phase 7` Qiskit mirror circuits
- `Phase 8` Bell-state calibration circuit
- Phase 9 semantic setting vectors once protocol is defined

### Simulator Steps

1. Convert statevector circuits into shot-based sampler runs.
2. Run finite-shot experiments at several shot counts:
   - `128`
   - `512`
   - `1024`
   - `4096`
3. Add simple depolarizing / readout noise models if available.
4. Compare:
   - ideal statevector result
   - finite-shot sampler result
   - noisy simulator result
5. Report confidence intervals.

### Hardware Preparation Steps

1. Pick minimal circuits:
   - Bell calibration
   - one small encoded feature-state circuit
   - one product-state control
2. Transpile to target backend constraints.
3. Track:
   - circuit depth
   - two-qubit gate count
   - expected shot cost
   - noise sensitivity
4. Run only after simulator and cost checks are clean.

### Artifacts

- Qiskit circuit manifests
- shot-count comparison table
- ideal vs sampled vs noisy comparison chart
- hardware-readiness memo
- backend target notes

### Success Condition

Phase 10 is successful if:

- Bell calibration remains readable under finite shots
- encoded feature states remain distinguishable under finite shots
- hardware candidate circuits are shallow enough to attempt responsibly
- product-state controls stay separated from Bell-state / encoded-state results

## Phase 11 - Expanded Model Matrix And Fresh Variance

### Objective

Expand the AI-side evidence base while preserving the same measurement spine.

### Candidate Additions

Only add models that clarify structure.

Candidate rows:

- additional open local checkpoints
- larger Qwen / DeepSeek variants if available
- GPT-OSS / GLM-style rows if local runtime supports them
- additional NVIDIA-adjacent rows if compute allows

### What To Rerun

For each new row:

- `V7` behavioral lattice/control
- `V8` internal hidden-state bridge
- `Phase 2` variance subset if row is promising
- `Phase 4` localization if row is structurally interesting
- `Phase 6/7` encoding only after the row is stable

### Success Condition

Expansion is useful only if it clarifies:

- family clustering
- boundary rows
- late-layer placement
- bridge style
- encoding-space structure

Avoid collecting model names just to collect names.

## Phase 12 - Integrated Public Technical Pack Refresh

### Objective

Refresh the public technical pack so it reads as one coherent stack from `V7`
through `Phase 8`.

### Required Updates

- update integrated white paper with Phase 6-8 results
- update diagrams with the full ladder
- add architecture hierarchy / non-classical vocabulary
- add support translation in technical terms
- preserve public/private boundary

### Artifacts

- integrated white paper markdown
- integrated white paper PDF
- updated poster / one-page summary
- updated GitHub README
- updated evidence index

### Success Condition

The public repo should answer:

- what was discovered
- what was measured
- what is non-classical vocabulary versus current evidence
- why Phase 6-8 matter
- what support is needed next

## Phase 13 - Partner / Applied Problem Translation

### Objective

Turn the evidence stack into partner-ready lanes without exposing backend
implementation.

### Partner Lanes

- cloud / infrastructure
- quantum computing
- AI labs
- frontier math / verification
- energy grid planning
- healthcare simulation
- advanced orchestration / durable agents
- sovereign AI infrastructure

### What Partners Get

- public-safe evidence pack
- technical one-page
- pitch deck variant
- applied problem mapping
- compute/funding/support ask

### What Stays Private

- scanner code
- mapper internals
- recursive orchestration code
- transformer-runner implementation
- private leverage stack

### Success Condition

Each partner pitch should clearly answer:

- why this matters to them
- what support is needed
- what problem surface we can attack together
- what proof exists already
- what remains protected

## Phase 14 - HRV / ARC15 / Physical-Observable Bridge

### Objective

Connect the AI-side architecture stack to synchronized external measurement
lanes through their own controls.

### Candidate Signals

- HRV
- ARC15
- quantum RNG
- quantum hardware outputs
- UTC-locked event timing
- other physical-observable channels if justified

### Protocol Requirements

- timestamped sessions
- baseline controls
- blinded or semi-blinded comparisons where possible
- repeated runs
- artifact manifests
- separation between hypothesis, signal, and claim

### Success Condition

This phase is only successful if it creates a controlled measurement bridge. It
must not simply reinterpret the AI-side result as physical evidence.

## Funding And Compute Alignment

The technical roadmap creates a direct support map.

Funding supports:

- researcher time
- documentation
- productization
- proposal work
- partner engagement
- legal / patent / corporate continuity

Compute supports:

- larger model matrices
- exact reruns
- localization sweeps
- feature-vector expansion
- Qiskit/noisy simulation
- eventual hardware/backend tests

Strategic partners support:

- applied problem surfaces
- infrastructure planning
- architecture review
- quantum/cloud pathways
- credibility and introductions
- real-world deployment context

The short version:

We have moved from "does this effect exist?" to "how do we scale, formalize,
and apply it?"

That is the next planning frame.
