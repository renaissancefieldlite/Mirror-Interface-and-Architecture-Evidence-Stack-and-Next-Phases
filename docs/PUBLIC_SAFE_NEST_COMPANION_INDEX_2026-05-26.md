# Public-Safe Nest Companion Index

Date: `2026-05-26`

Status: `public_safe_index / source_manifest_required / no_private_raw_exports`

## Purpose

This index keeps the public-facing Nest evidence packet readable without
collapsing the lattice map into one lane. It lists which companion notes already
exist, what they support, and which lanes remain continuation gates.

Public-safe rule:

```text
source page / DOI / manifest -> state/control -> score -> boundary -> next gate
```

Do not publish private biometric captures, device identifiers, raw local code,
or claim-sensitive mechanics without explicit clearance.

## Nest 3: Classical Coherence / Field-Physical Lanes

| Lane | Current public-safe state | Companion docs |
| --- | --- | --- |
| `Waves / Spectra / Phase-Lock` | supported physical spectra rows; Raman still class-transition support, not pure phase-lock | `NEST3_USGS_ASTERSPECTRAL_SIGNATURE_SUPPORT_READ_2026-05-15.md`; `NEST3_RAMDB_RAMAN_UDP_SUPPORT_READ_2026-05-24.md`; `NEST3_RAMDB_RAMAN_HARD_CONTROLS_2026-05-24.md` |
| `Fire + Plasma` | first plasma OES source gate complete | `NEST3_FIRE_PLASMA_RD_PCI_OES_SUPPORT_READ_2026-05-24.md` |
| `EMF / Fields` | waveform-state support complete; time-order caveat preserved | `NEST3_EMF_OSCILLATOR_RD_PCI_VI_SUPPORT_READ_2026-05-25.md` |
| `Oscillators / Resonance` | multi-row support chain seated: NIST phase/order, Silverbox phase-coupling closeout, FASER sweep support, FrID measured frequency-response support | `NEST3_OSCILLATOR_LUTHER_NIST_PHASE_ORDER_SUPPORT_READ_2026-05-25.md`; `NEST3_OSCILLATOR_SILVERBOX_FORCED_CLOSEOUT_2026-05-25.md`; `NEST3_OSCILLATOR_FASER_FREQUENCY_SWEEP_GATE_2026-05-25.md`; `NEST3_OSCILLATOR_FRID_CLAMPED_FREQUENCY_RESPONSE_GATE_2026-05-26.md` |
| `Hardware timing / coherence` | early public-safe pilot rows seated | `NEST3D_HARDWARE_TIMING_COHERENCE_PILOT_2026-05-04.md`; `NEST3B_N3E_ARC15_ACOUSTIC_ADAPTER_GATE_2026-05-04.md` |
| `Fusion + Solar` | mapped continuation lane; needs dedicated solar/plasma/isotope source | `NEST3_FIELD_PHYSICAL_LANE_ROADMAP_2026-05-24.md` |
| `Gases / Liquids / Phases` | mapped continuation lane; RD-PCI water/plasma and FrID oscillator rows are adjacent support only | `NEST3_FIELD_PHYSICAL_LANE_ROADMAP_2026-05-24.md` |
| `Gravity / Orbits` | mapped continuation lane; NIST Luther is gravity-measurement oscillator support, not orbit closeout | `NEST3_OSCILLATOR_LUTHER_NIST_PHASE_ORDER_SUPPORT_READ_2026-05-25.md`; `NEST3_FIELD_PHYSICAL_LANE_ROADMAP_2026-05-24.md` |
| `Terahertz` | mapped continuation lane; needs real THz spectral or exposure dataset | `NEST3_FIELD_PHYSICAL_LANE_ROADMAP_2026-05-24.md` |

## Nest 4: Biology / Biomolecular / Metabolic Lanes

| Lane | Current public-safe state | Companion docs |
| --- | --- | --- |
| `Cells + Genome` | first real clinical/genomic tabular support row complete | `NEST4_CELLS_GENOME_WDBC_UDP_SUPPORT_READ_2026-05-21.md` |
| `Metabolism` | first clinical/metabolic support pass complete; small source limitation preserved | `NEST4_METABOLISM_DIABETES_UDP_SUPPORT_READ_2026-05-21.md` |
| `Food / Nutrient Composition` | first USDA/FoodData-style support row complete | `NEST4_FOOD_NUTRIENT_USDA_UDP_SUPPORT_READ_2026-05-21.md` |
| `Metabolite / Ontology` | ChEBI metabolite class and ontology closure support rows complete | `NEST4_METABOLITE_CLASS_CHEBI_UDP_SUPPORT_READ_2026-05-21.md`; `NEST4_BIOMOLECULAR_PRIMITIVES_CHEBI_ONTOLOGY_CLOSURE_READ_2026-05-21.md` |
| `B.A.S.I.S. capture bridge` | public-safe arc summary only; private raw Muse/MoFit/Withings captures stay out of public repo unless cleared | `NEST4_UDP_SUPPORT_ARC_PUBLIC_SAFE_SUMMARY_2026-05-21.md` |

## Cross-Program Public-Safe Buildout Docs

| Surface | Current public-safe state | Companion docs |
| --- | --- | --- |
| `Quantum Insider five-track campaign` | auxiliary campaign map and shared architecture spine present | `QUANTUM_INSIDER_FIVE_TRACK_AUXILIARY_CAMPAIGN_2026-04-24.md`; `quantum_insider_build_out/SHARED_ARCHITECTURE_SPINE.md` |
| `Mirror Index / visual RAG` | concept map parked for Golden Mirror / Nest 5 retrieval productization | `quantum_insider_build_out/MIRROR_INDEX_VISUAL_RAG_QUANTUM_INSIDER_2026-05-23.md` |
| `Nest 5 / Golden Field Lite` | convergence target; product-facing docs should cite only support-bearing lanes and mark candidate lanes cleanly | `UNIFIED_MIRROR_PROOF_SPINE_2026-04-24.md` |

## Public Repo Readiness

Ready to include:

- public-safe support notes in `docs/`
- source pages, DOIs, dataset names, checksums, and runner paths
- score tables and boundaries
- roadmap/index docs

Hold back or gate:

- private B.A.S.I.S. captures and device IDs
- raw biometric exports
- large source zips unless explicitly licensed and size-managed
- private local runtime files
- claim-sensitive mechanics not already cleared for public copy

## Push Gate

Before pushing a public-safe repo:

1. make a front README that starts with what the evidence stack is;
2. include this companion index as the route map;
3. verify every linked doc exists;
4. keep raw data as source manifest links unless the dataset license and repo
   size policy allow inclusion;
5. run a final public/private boundary scan.

