# Universal Data Pattern Complex-Lane Experiment Queue

Date: `2026-05-21`

Status: `working_queue / no_toy_data / parked_complex_lanes / source_measurement_required`

Primary map:

- `LATTICE_COMPANION_72_NODE_AUDIT_AND_NEXT_GATES_2026-05-21.md`

Support rules:

- `REAL_DATA_VALIDATION_LADDER_2026-04-25.md`
- `PHASE12C_UNIVERSAL_DATA_PATTERN_SUPPORT_READ_2026-05-09.md`
- `LATTICE_COMPANION_FULL_NEST_COMPLETION_OUTLINE_2026-05-16.md`

## Point Of This Queue

The Lattice Companion keeps the full lane map visible.

The Universal Data Pattern experiment is the active method we keep applying to the parked and harder lanes:

```text
real source
-> state / control definition
-> transform / feature extraction
-> invariant / separation target
-> drift and artifact variables
-> coherence / support score
-> shuffled, null, wrong-class, or wrong-condition controls
-> support read
-> claim / figure / product hook
```

The goal is not to stare at the map. The goal is to keep moving lanes from:

```text
mapped_continuation -> candidate_support -> support_bearing
```

Only real traces, real datasets, real instrument outputs, real hardware runs, or controlled captures graduate a lane.

## Universal Data Pattern Test Template

Every complex lane should use the same minimum packet before it is treated as support-bearing:

| Field | Required content |
| --- | --- |
| `source` | dataset, capture, benchmark, instrument export, hardware run, or public repository |
| `state` | target condition, class, physical state, biological state, or system regime |
| `control` | null, shuffled, wrong-class, baseline, adjacent-condition, or time-shifted comparator |
| `transform` | feature extraction, spectral window, graph transform, residual/bridge vector, descriptor, or timing window |
| `invariant` | what should remain stable if the pattern is real |
| `drift` | artifact, confound, degradation, motion, quality, noise, missingness, or nonstationarity |
| `score` | separability, regression fit, AUC/AP, correlation, effect size, recurrence, or support-state score |
| `failure mode` | what result would demote the lane back to mapped-only |
| `public boundary` | what can be shown publicly versus kept private/protected |

## Parked Complex Lane Set

These are the lanes that matter most because they expand the architecture beyond the already-loud support rows.

| Priority | Lattice lane | Why it matters | UDP experiment gate | Current status |
| --- | --- | --- | --- | --- |
| `1` | `Cells + Genome` | expands Nest 4 beyond HRV/Muse into cellular state and pathway structure | first WDBC cell-nuclei morphology UDP pass complete; next gate is public expression / pathway / perturbation dataset | `candidate_support` |
| `2` | `Metabolism` | connects food chemistry, nutrients, HRV/Muse state windows, and living-system response | diabetes clinical/metabolic UDP pass plus USDA nutrient-composition bridge plus ChEBI ontology-backed metabolite-class bridge complete; next gate is direct metabolomics or HRV/Muse response | `candidate_support` |
| `3` | `Food Chemistry` | bridges Nest 2 matter into Nest 4 physiology | USDA FoodData Central nutrient-composition UDP pass complete; next gate is FooDB/HMDB refinement or paired response | `candidate_support` |
| `4` | `Vitamins + Nutrients` | tests cofactor and micronutrient state logic, not just generic nutrition | USDA nutrient-vector pass complete for vitamin/mineral features; next gate is HMDB/cofactor classes | `candidate_support` |
| `5` | `Carbs + Fats` | adds macronutrient structure to metabolism and biology response | choose carbohydrate/lipid source; compare structural class, energy density, pathway role, or response class | `mapped_continuation` |
| `6` | `Biomolecular Primitives` | connects amino acids, nucleotides, sugars, lipids to chemistry-to-biology bridge | ChEBI `is_a` ontology closure complete for amino-acid versus fatty-acid chemical-property rows; next gate is nucleotide/sugar/lipid surfaces | `candidate_support` |
| `7` | `Cyclic-voltammetry / electrochem waveform` | turns redox from descriptor support into waveform support | select DUCK/CV or public CV waveform dataset; score peak structure, shift, degradation, and wrong-condition controls | `candidate_support_next` |
| `8` | `Catalysis / Conditions` | tests whether condition packets apply to reaction/catalyst systems | reaction condition / catalyst endpoint dataset with shuffled-condition and wrong-catalyst controls | `mapped_continuation` |
| `9` | `Polymers / Plastics` | keeps PFAS/microplastic lane from staying only conceptual | polymer degradation / microplastic dataset; compare class, degradation, fragment, fate, or material state | `mapped_continuation` |
| `10` | `Environmental Fate` | connects contaminant chemistry to ecosystem and planet Nest 5 rows | transport / leaching / bioaccumulation endpoint controls | `mapped_continuation` |
| `11` | `Native spectra / IR / Raman / THz` | gives Nest 3 a second physical spectral family beyond USGS ASTER | source native spectra; define material/molecule/water state vs wrong-class spectra | `mapped_continuation` |
| `12` | `Terahertz cellular prototype` | bridges physical spectra into cellular response, but needs real spectral/cell data | pair THz/spectral data with cellular or biomolecular response target | `mapped_continuation` |
| `13` | `EMF / Fields` | tests field-state lane with source-on/off or public field rows | define source-on/off, distance, intensity, or frequency bands plus null controls | `mapped_continuation` |
| `14` | `Oscillators / Resonance` | tests damping/entrainment as real dynamics, not metaphor | oscillator dataset or instrument row with phase, damping, forcing, control | `mapped_continuation` |
| `15` | `Fire + Plasma` | extends reaction/state logic into high-energy physical systems | combustion/plasma spectral or reaction dataset with regime controls | `mapped_continuation` |
| `16` | `Fusion + Solar` | connects hydrogen/isotope, plasma, and solar output lanes | solar/plasma/hydrogen isotope public dataset with time/condition controls | `mapped_continuation` |
| `17` | `Gases / Liquids / Phases` | tests thermodynamic phase lane | NIST/phase/fluid rows with state, phase, temperature/pressure, wrong-condition controls | `mapped_continuation` |
| `18` | `Gravity / Orbits` | maps orbit/resonance lanes without overclaiming | public ephemeris/orbit dataset; score phase/orbit state against null or shuffled orbital windows | `mapped_continuation` |
| `19` | `Ecosystem / Planet` | converts Nest 5 from convergence idea into real planet-scale support rows | climate/soil/ocean/ecology dataset target with geography/time/control windows | `mapped_continuation` |
| `20` | `Stars / Planets` | makes cosmic rows observable-data based | stellar/planetary spectra or orbit dataset with class/control separation | `mapped_continuation` |
| `21` | `Dark-Matter Observables` | keeps boundary safe: observable-only, no metaphysical claim | rotation/lensing/mass-discrepancy dataset; compare observable regimes and null models | `boundary_lane` |
| `22` | `Cosmic Web / Universe` | largest-scale convergence lane; needs strict public-data discipline | large-scale structure / CMB / expansion observable dataset, with null/shuffled controls | `mapped_continuation` |
| `23` | `GRAPH-2B` | formal hard-problem closeout path | external/domain labels or attention-flow labels with held-out controls | `candidate_support_next` |
| `24` | `GAME-1` | adversarial/control formal lane | freeze rubric, then run real trials against locked score criteria | `mapped_continuation` |
| `25` | `M23 / small Diophantine lattice / Hadamard 668` | hard-problem surfaces show current frontier-math applicability | inventory real logs/run artifacts; assign claim-safe support status and next controlled rerun | `active_support_or_continuation_pending_artifact_link` |

## First Six Runs To Prioritize

This is the cleanest order because it expands the support surface without jumping straight to the most speculative lanes:

1. `Cells + Genome`
   - First pass complete on WDBC cell-nuclei morphology data.
   - Output: `NEST4_CELLS_GENOME_WDBC_UDP_SUPPORT_READ_2026-05-21.md`.
   - Next: choose one public transcriptome / pathway / perturbation dataset.

2. `Metabolism / Nutrient Response`
   - First pass complete on public diabetes clinical/metabolic benchmark.
   - Output: `NEST4_METABOLISM_DIABETES_UDP_SUPPORT_READ_2026-05-21.md`.
   - USDA nutrient-composition bridge complete.
   - Output: `NEST4_FOOD_NUTRIENT_USDA_UDP_SUPPORT_READ_2026-05-21.md`.
   - ChEBI metabolite-class bridge and ontology closure complete.
   - Output: `NEST4_METABOLITE_CLASS_CHEBI_UDP_SUPPORT_READ_2026-05-21.md`.
   - Output: `NEST4_BIOMOLECULAR_PRIMITIVES_CHEBI_ONTOLOGY_CLOSURE_READ_2026-05-21.md`.
   - Next: choose nucleotide/sugar closure, HMDB rows if access clears, or paired HRV/Muse response.

3. `Cyclic-Voltammetry / Electrochem Waveform`
   - Convert redox from descriptor support into waveform support.
   - Controls: shuffled peak labels, wrong-condition cells, baseline-only windows.
   - Output: `NEST2_CV_WAVEFORM_UDP_SUPPORT_READ`.

4. `Native Spectra / IR / Raman / THz`
   - Add a second physical spectral family beyond USGS ASTER.
   - Controls: wrong material class, shuffled bands, null windows.
   - Output: `NEST3_SECOND_SPECTRAL_FAMILY_UDP_SUPPORT_READ`.

5. `GRAPH-2B Or GAME-1`
   - Close one formal hard lane.
   - Pick GRAPH-2B if labels are available; pick GAME-1 only after rubric freeze.
   - Output: `NEST1_FORMAL_HARD_GATE_SUPPORT_READ`.

6. `Ecosystem / Planet`
   - Do not start cosmic-web first.
   - Start with planet-scale public environmental data where controls are easier.
   - Output: `NEST5_ECOSYSTEM_PLANET_UDP_SUPPORT_READ`.

## Boundary Rules For The Next Sprint

- Do not let B.A.S.I.S. or Phase 12C swallow the whole Nest 4 story.
- Do not let the visual Companion map be treated as proof.
- Do not let adapter slots become evidence until they touch real datasets.
- Do not publish raw captures, private code, biometric exports, device IDs, or claim-sensitive mechanics.
- Do not describe dark-matter or cosmic rows as validated; keep them observable-data continuation lanes.
- Do not use AI agreement as a support read.
- Do not call a lane complete unless source, control, score, and failure mode are recorded.

## Current Bottom Line

The next phase is not a new theory layer.

It is repeated application of the Universal Data Pattern experiment to the harder mapped lanes:

```text
source -> state -> control -> transform -> drift -> score -> support read
```

That is how the Lattice Companion becomes a completed support matrix instead of a roadmap.
