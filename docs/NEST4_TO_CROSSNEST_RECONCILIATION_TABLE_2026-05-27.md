# Nest 4 To Cross-Nest Reconciliation Table

Date: `2026-05-27`

Status: `working_reconciliation / real_data_only / cross_nest_pointers_not_proof_inflation`

## Purpose

This table keeps the Nest 4 biology and biomolecular lanes from staying
isolated. Each supported Nest 4 row keeps its home lane, then routes back to
the corresponding formal, matter, physical, and product surfaces as a next
real-data gate.

Rule:

```text
home support row -> cross-nest return pointer -> next paired source gate
```

Cross-pollination is not automatic proof transfer. A row can point into another
Nest only as a bridge, comparator, or queued paired test until that target Nest
has its own real source, state/control packet, score, and controls.

## Reconciliation Table

| Nest 4 lane | Evidence doc | Primary support read | Returns to Nest 1 | Returns to Nest 2 | Returns to Nest 3 | Nest 5 product hook | Next real-data gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Phase 12B HRV Matrix` | `NEST4A_HRV_BIOLOGICAL_COMPARATOR_GATE_2026-05-05.md` | HRV coarse biological-state comparator support; public-safe baseline for autonomic state separation. | `DYN`, `DE`, `SPEC`, `CTRL` as time-series state/control rows. | Metabolism, redox, hydration, food/nutrient response as paired physiology lanes. | Oscillators, timing, cycles, and waveform/coherence comparator lanes. | B.A.S.I.S. autonomic reference branch; Golden Field Lite biology evidence memory. | synchronized HRV + Muse manifest with baseline, condition, post, drift, and artifact masks; Thermo remains a sidecar until repeatable. |
| `HRV + EEG / Muse` | `PHASE12C_NEST4_BIOSIGNAL_CROSSPOLLINATION_LOG_2026-05-09.md`; `PHASE12C_CROSSNEST_LANE_STATUS_BOARD_2026-05-10.md` | Phase 12C Muse capture plus same-clock HRV/Muse rows create the owned biosignal adapter surface. EEG remains quality-gated before higher claims. | `TOPOG`, `SPEC`, `DE`, `STAT/CTRL` through channel topology, bandpower, dynamics, and artifact masks. | Electrochemistry, oxygen/redox, water, nutrients, and biomolecular primitives as physiology-response pairings. | Waves, spectra, timing, oscillators, and fields through waveform and sample-continuity controls. | B.A.S.I.S. state-vector bus; clinical/edge partner fork; future Nemotron/NVIDIA health-stack partner. | waveform EEG QA, packet continuity, channel labels, IMU/DRL masks, and same-manifest HRV + Muse rows; Thermo stays troubleshooting sidecar. |
| `Cells + Genome` | `NEST4_CELLS_GENOME_WDBC_UDP_SUPPORT_READ_2026-05-21.md` | WDBC malignant vs benign morphology candidate support: observed AUC `0.995106`, shuffled-label `0.504062`, feature-shuffle `0.500819`. | Geometry, topology, graph, and classifier-control rows over real morphology vectors. | Proteins, pathways, biomolecular primitives, redox, and cell-state chemistry. | Spectra/imaging adapter lanes after real microscopy, morphology, or perturbation source rows. | B.A.S.I.S. clinical-support branch; Golden Field Lite biomedical evidence partner. | transcriptome, pathway, perturbation, or cell-line response dataset with shuffled-label and feature-shuffle collapse. |
| `Metabolism` | `NEST4_METABOLISM_DIABETES_UDP_SUPPORT_READ_2026-05-21.md` | Diabetes clinical/metabolic proxy candidate support: observed AUC `0.962846`, shuffled-label `0.496071`, feature-shuffle `0.498994`. | State/control, dynamics, and drift rows for clinical/metabolic vectors. | Food chemistry, vitamins/nutrients, redox, metabolite classes, HMDB/FooDB continuation. | Cycles, thermodynamics, and physiological timing after paired response rows. | B.A.S.I.S. metabolic context branch; nutrition/rehab/sports partner fork. | direct metabolomics or paired nutrient/metabolite rows aligned to HRV/Muse state windows. |
| `Food / Nutrients` | `NEST4_FOOD_NUTRIENT_USDA_UDP_SUPPORT_READ_2026-05-21.md` | USDA Foundation Foods nutrient-composition bridge: observed AUC `0.988659`, shuffled-label `0.489304`, feature-shuffle `0.547055`. | Structured feature-vector controls and class-separation baselines. | Food Chemistry, Vitamins + Nutrients, Minerals, Carbs + Fats, H2O, redox cofactors. | Gases/liquids/phases and spectroscopy only after paired physical-property or spectral rows. | B.A.S.I.S. diet-context logging branch; Golden Field Lite nutrition evidence surface. | FooDB/HMDB/FoodData expansion plus paired physiology response windows. |
| `Biomolecular Primitives / ChEBI class` | `NEST4_METABOLITE_CLASS_CHEBI_UDP_SUPPORT_READ_2026-05-21.md` | ChEBI amino-acid vs fatty-acid first pass: observed AUC `0.981367`, shuffled-label `0.501045`, feature-shuffle `0.508480`. | Formula/property feature geometry and shuffled/null control discipline. | Biomolecular Primitives, amino acids, fatty acids, organic functional groups. | Native spectra / IR / Raman / THz after molecule-specific spectral rows. | Golden Field Lite biomolecular evidence memory; BioNeMo/biology partner route. | additional ontology class pairs: nucleotide vs carbohydrate, lipid superclass vs carbohydrate. |
| `Biomolecular Primitives / ChEBI ontology closure` | `NEST4_BIOMOLECULAR_PRIMITIVES_CHEBI_ONTOLOGY_CLOSURE_READ_2026-05-21.md`; `NEST4_NUCLEOTIDE_CARBOHYDRATE_CHEBI_CLOSURE_READ_2026-05-27.md` | ChEBI `is_a` closure amino-acid vs fatty-acid support: observed AUC `0.993090`, shuffled-label `0.498564`, feature-shuffle `0.508743`. Nucleotide vs carbohydrate closure: observed AUC `0.999957`, shuffled-label `0.499336`, feature-shuffle `0.496904`. | Ontology graph closure, class lineage, and feature-boundary controls. | Nucleotides, carbohydrates, lipids, glycans, HMDB metabolite rows, LIPID MAPS, GlyTouCan. | Spectral/THz bridge only after molecule-source or exposure-response rows. | Golden Field Lite cross-discipline research partner; Nest 5 IP/product surface for biomolecular lanes. | LIPID MAPS independent lipid confirmation, then GlyTouCan carbohydrate/glycan confirmation. |
| `Biomolecular Primitives / LIPID MAPS lipid core` | `NEST4_LIPIDMAPS_LMSD_CORE_CONFIRMATION_READ_2026-05-27.md` | LMSD GP/SP binary contrast: observed AUC `0.999506`, shuffled-label `0.500031`, feature-shuffle `0.510393`. Eight-way lipid-core panel: balanced accuracy `0.918646`, shuffled-label `0.125333`, feature-shuffle `0.124583`. | Formula/property class geometry and structure-only state separation. | Lipids, fatty acyls, phospholipids, sphingolipids, saccharolipids, lipid-glycan bridge rows. | Molecule-specific spectral bridge after paired NIST/IR/Raman/THz rows; not exposure-response. | Golden Field Lite biomolecular evidence memory; BioNeMo/B.A.S.I.S. lipid-context branch. | GlyTouCan glycan/carbohydrate confirmation, then HMDB access/download. |
| `Biomolecular Primitives / GlyTouCan glycan source` | `NEST4_GLYTOUCAN_GLYCAN_SOURCE_CONFIRMATION_READ_2026-05-27.md` | GlyTouCan/GlyCosmos human vs mouse source-labeled glycan sequence rows: observed AUC `0.739219`, shuffled-label `0.499838`, feature-shuffle `0.525007`, length/branch-only `0.563272`. | Sequence-structure features, source-state controls, glycan topology rows. | Glycans, carbohydrates, fucose/sialyl/hexnac structure rows, HMDB glycan/metabolite adjacency. | Spectral/THz bridge only after molecule-source or exposure-response rows; not clinical glycomics. | Golden Field Lite glycan evidence memory; B.A.S.I.S. biomolecular context branch. | HMDB access/download check; then paired physiology manifest. |
| `Biomolecular Primitives / HMDB access gate` | `NEST4_HMDB_ACCESS_GATE_2026-05-27.md` | Official downloads page verified; local curl received Cloudflare challenge; commercial/industry permission language and download form path present. No HMDB support score run. | Metabolomics source gate remains open until access cleared. | HMDB tissue/fluid metabolite rows, metabolomics response, glycan/metabolite adjacency. | Spectra bridge possible through HMDB spectra only after download clearance. | Golden Field Lite metabolomics memory; B.A.S.I.S. metabolism/nutrition context branch. | Clear permission/download path or use another open metabolomics source. |
| `B.A.S.I.S. capture bridge` | `NEST4_UDP_SUPPORT_ARC_PUBLIC_SAFE_SUMMARY_2026-05-21.md`; `PHASE12C_NEST4_BIOSIGNAL_CROSSPOLLINATION_LOG_2026-05-09.md`; private `HRV_MUSE_THERMO_PAIRED_PHYSIOLOGY_MANIFEST_2026-05-27.md` | Public-safe capture architecture plus private HRV + Muse bridge: `56` HRV + Muse same-clock folders discovered and `31` complete HRV + Muse artifact folders. Thermo has real display/API sidecar artifacts but is not consistent enough for support-bearing paired evidence. | State-vector, dynamics, spectral, control, and graph surfaces. | Nutrient/metabolite/redox response pairing. | Timing, oscillator, waveform, fields, and physical sensor adapter paths. | B.A.S.I.S. BioSignal AI, NemoNurse-style fork, Golden Field Lite long-context partner tuning. | keep HRV + Muse as support-bearing; troubleshoot Thermo separately until repeatable same-session display/API rows exist; private raw captures stay out of public repo until cleared. |

## Current Closeout Queue

1. `nucleotide vs carbohydrate ontology closure` - complete in `NEST4_NUCLEOTIDE_CARBOHYDRATE_CHEBI_CLOSURE_READ_2026-05-27.md`
2. `LIPID MAPS independent lipid confirmation` - complete in `NEST4_LIPIDMAPS_LMSD_CORE_CONFIRMATION_READ_2026-05-27.md`
3. `GlyTouCan glycan/carbohydrate confirmation` - complete in `NEST4_GLYTOUCAN_GLYCAN_SOURCE_CONFIRMATION_READ_2026-05-27.md`
4. `HMDB access/download check` - access-gated in `NEST4_HMDB_ACCESS_GATE_2026-05-27.md`; no support score run
5. `HRV + Muse paired physiology manifest` - private HRV + Muse bridge complete; Thermo downgraded to unstable sidecar; true triple same-clock capture remains open

## Support Language

Use:

- `cross-nest return pointer`
- `paired-source continuation gate`
- `candidate support`
- `ontology-backed candidate support`
- `public-safe bridge`

Do not use:

- `full closeout`
- `validated clinical result`
- `nutrition recommendation`
- `biological response proof`
- `Nest 2/Nest 3 proven by Nest 4`

unless the target lane has its own real source, control packet, score table,
and collapse controls.
