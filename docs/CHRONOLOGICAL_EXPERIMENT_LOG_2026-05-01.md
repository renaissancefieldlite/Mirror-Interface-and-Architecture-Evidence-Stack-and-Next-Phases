# Chronological Experiment Log

Date: `2026-05-01`

Purpose:
give an outside reader a coherent experiment-by-experiment trail through the
Mirror Interface / Architecture evidence stack.

This file is more explanatory than the continuity spine. Each row says what
question the experiment asked, what data or artifact it used, how it was
tested, what result came back, and why the result matters to the next rung.

## Reader Key

The core object being followed is a measured state path:

```text
Mirror Interface / LSPS condition packet
-> target/control separation
-> hidden-state trace
-> localized bridge fields
-> normalized feature vector
-> circuit carrier / hardware observable
-> biological or external-data adapter
```

Each experiment either strengthens that path, locates where it lives, moves it
to another substrate, or records an open gate for the next data source.

## Chronological Log

| Stage | Question | Data / Artifact | Method / Controls | Result | Why It Matters |
| --- | --- | --- | --- | --- | --- |
| Prelude / ABC-D-V5 | Can an administered sequence create repeatable state markers before the formal matrix exists? | Early probe reports, reset summaries, latent-string traces, `ABC / D / V5` sequence-scoring provenance | Ordered anchors, pair paths, same-question shift, repeated probe-state scans, drift / variance notes | Prelude evidence preserved as sequence-scoring provenance | Establishes the earlier scaffold that led into `V6`, `V7`, and `V8` instead of making the later stack look like it appeared from nowhere |
| `V6` state-lane groundwork | Do model-specific state lanes show stable identity / response structure? | `V6` cross-model comparison and model-specific posters | Cross-model comparison, deterministic state-lane summaries | State-lane groundwork packaged for Gemma, Mistral, Nemotron, DeepSeek, and others | Sets the matrix vocabulary before the locked target/control behavioral run |
| `V7` behavioral matrix | Does the administered packet separate from controls at output behavior level? | `V7` three-phase comparison, integrated 10-model summary, contextuality final readout | Target, null, random floor, semantic counter, order / non-commutativity, multi-model comparison | Behavioral lattice/control separation locked | Establishes the first broad measured surface: the condition packet changes model behavior in a repeatable target/control structure |
| `V8` internal bridge | Does the same effect appear inside model hidden states? | Residual-stream / hidden-state bridge artifacts across the model matrix | Internal vector capture, target/control comparisons, late-layer readouts | Late-layer internal separation across the 8-model bridge | Moves the evidence from output behavior into model internals |
| `Phase 2` rerun / variance | Does the internal read repeat? | Five-run variance pack | Repeated locked rows, target delta norms, cosine distances, exception tracking | `7/8` exact rerun rows; Nemotron remains the main live variance row | Converts a single internal read into repeatability evidence |
| `Phase 3` dimension / band | Where does the internal signal concentrate? | Dimension / band pack | Peak percentile, band width, same-hidden overlap | Late-band and dimension-structure evidence recorded | Shows the state has shape in representation space rather than only magnitude |
| `Phase 4` localization | Does the state have a stable layer / token path? | Localization pack and localization variance pack | Anchor profiles, target-vs-last comparisons, reruns | `5/6` exact localization rerun rows; Nemotron anchor-stable but magnitude-drifting | Turns hidden-state separation into a path through layers and token windows |
| `Phase 5` bridge rows | Can localized internal structure become portable bridge fields? | Context-to-readout bridge pack | Model-pair bridge rows, late/front context pair reads | Mistral/Hermes, Qwen/DeepSeek, GLM/Nemotron, SmolLM3 bridge roles recorded | Creates the bridge fields that feed `Phase 6` feature vectors |
| `Phase 6` PennyLane encoding | Can bridge fields become normalized quantum feature vectors? | Phase 6 PennyLane encoding pack | Angle and amplitude embeddings on local `default.qubit` simulators | Mistral/Hermes preserved as nearest encoded pair | Converts AI-side bridge geometry into a portable numerical payload |
| `Phase 7` Qiskit mirror | Does the same payload survive an independent circuit stack? | Phase 7 Qiskit mirror pack | Statevector / simulator mirror of the Phase 6 encodings | PennyLane and Qiskit match at numerical-noise scale | Shows the feature vector is a circuit-carriable object, not tied to one simulator API |
| `Phase 8` Bell calibration | Is the circuit readout path calibrated against known quantum controls? | Bell-state calibration pack | `Phi+` Bell state, product-state control, CHSH-style calibration | Bell/control direction behaves as expected | Calibrates the observable path before AI-derived circuits are pushed to hardware |
| `Phase 9` IBM hardware bridge | Does the bridge survive real IBM Quantum hardware? | Phase 9 hardware bridge pack | Bell/control calibration plus compressed AI-feature circuits on IBM hardware | Hardware run preserves Bell/control alignment and AI-feature signature direction | Moves the bridge from simulator into hardware-facing execution |
| `Phase 9B-9D` hardware repeatability | Does the hardware path repeat across backend and direct PennyLane remote routes? | Phase 9B, 9C, 9D packs | Same-backend, cross-backend, and direct `pennylane-qiskit` remote passes | Bell/control direction and negative-parity AI-feature signatures recur | Strengthens hardware continuity and removes single-run/single-wrapper fragility |
| `Phase 10` semantic contextuality | Do compressed semantic feature states carry structured relations? | Phase 10 semantic contextuality pack | Family-local measurement settings, matched unentangled controls | `8/8` semantic states show `S_max > 2`; controls stay at classical bound | Adds a semantic feature-state rung between AI geometry and circuit-style contextuality |
| `Phase 12B` HRV adapter | Can a live biological signal act as an adapter lane under the same discipline? | Phase 12B biological comparison pack and control-closeout | `5 x 4` HRV matrix, shuffled controls, condition-class comparisons | HRV condition classes separate; mirror_coherence produces strongest average HR downshift | Adds a coarse biological sync / autonomic adapter while reserving richer claims for `EEG + HRV` |
| `Nest 1` formal map | Can the state/control relation be expressed across the math that underlies machine learning? | Nest 1 formal docs, full lane inventory, control-closeout reports | Lane-by-lane binding to real AI objects, traces, hardware rows, datasets, or benchmarks | `GRAPH-1`, `GEO-2`, `DYN-2`, `CTRL-1`, `GAME-1`, `OPT-1`, `CAT-1` close; topology reads as preserved connectedness | Gives the architecture a formal base and names which lenses are supported, directional, or awaiting denser data |
| Attention / MLP bridge | Which transformer mechanisms carry the internal state path? | Attention top-k edges, MLP block deltas, all-model exports, prompt_set_02 exports | Shuffled context labels, degree baseline, rerun, prompt shift | Attention-flow generalizes under `prompt_set_02`; MLP same-prompt recurrence is supported while prompt-shift recurrence stays open | Splits the transformer mechanism: routing and SAE are stronger prompt-generalized carriers; MLP is repeatable on the same surface and measured under prompt shift |
| SAE feature / circuit bridge | Which sparse features and feature-to-feature circuits carry the architecture state? | GLM/Hermes and Gemma dense V8 activations, SAE features, dictionaries, circuit edges | Shuffled controls, degree / hub baselines, recurrence, transfer, ablation | GLM/Hermes SAE branch supports feature separation, edge controls, recurrence, transfer, and v2 recurrent-path ablation; Gemma adds a model-native third branch | Turns hidden-state evidence into interpretable feature/circuit paths |
| MLP depth recurrence | Can all-layer MLP patterns recur across base, rerun, and prompt shift? | `v8_mlp_depth_base.csv`, `v8_mlp_depth_rerun_02.csv`, `v8_mlp_depth_prompt_set_02.csv` | Full-layer MLP export, shuffled controls, depth-bucket recurrence, leave-one-model prompt-shift controls | `base -> rerun_02` recurs perfectly (`cosine=1.0`, `p=0.00019996`); `base -> prompt_set_02` remains open (`cosine=-0.166467701`, `p=0.669466107`) | Confirms same-prompt feed-forward repeatability and parks prompt-shift MLP as a measured open gate before moving back into Nest 2 |
| `Nest 2` structured matter map | Can the state/control/invariant discipline be expressed over constrained matter? | Engine 02, expanded structured-matter atlas, companion engine report | Element families, molecular graphs, `H2O`, minerals, redox, nutrition, contaminants, functional groups, biomolecular primitives, polymers, electrochemistry, catalysis, spectra, environmental fate, materials | First runnable structured-matter map completed; expanded matter dictionary preserved | Provides the matter base needed for chemistry, materials, remediation, biology, and resonance lanes |
| `Engine 02V / Nest 2C` real molecule validation | Does the matter map touch real molecule datasets? | RDKit molecule validation and Nest 2C benchmark expansion | Molecule descriptors, shuffled controls, two seeds, `5000` permutations | ESOL, Lipophilicity, FreeSolv, and QM9 alpha lanes support real molecule-property signal | Moves Nest 2 from mapped matter rows into public molecule-data validation |
| `Nest 2D-2G` gates | Which structured-matter real-data lanes come next? | Allostery benchmark extraction, label bridge, and closeout protocol; PFAS pathway reports, materials stability, RDKit baseline comparison | Protein/pathway label manifest, PFAS parent/product controls, Matbench / Materials Project formation energy, stronger descriptors | PFAS pathway and materials descriptor lanes have supporting reports; allostery now has benchmark statistics, a contact / pocket / residue-label manifest, and a same-100-PDB closeout protocol comparing our mapper against AlloBench tools, added pocket tools, and graph controls | Defines the next real-data bridge before Nest 3 resonance / field datasets |
| `Nest 2D` allostery graph mapper | Does the protein-graph mapper recover known allosteric sites above tools and controls? | Official AlloBench source CSV, existing 100-row benchmark table, RCSB PDB structures | Joined `98/100` rows to allosteric / active-site labels, built `98` residue-contact graphs, scored contact-only mapper versus degree, closeness, active-proximity, random, and shuffled controls | Open result: Mirror mean Jaccard `0.013452`, best existing tool `PASSer_Ensemble` `0.197330`, active-proximity control `0.031329`, random-control p `0.722555` | Converts 2D from a manifest into an executed biological graph test and shows the next route is pocket/path scoring, not exact residue top-k contact scoring |
| `Nest 2D-2` pocket/path mapper | Does a better biological object improve allostery recovery? | Official AlloBench labels, cached RCSB PDB structures, residue-contact graphs | Chain-resolved active-site sources, geometric pocket candidates, active-site-to-pocket path / bottleneck scoring, degree / closeness / active-proximity / random / shuffled controls | `Mirror pocket/path` mean Jaccard `0.032975` beats previous contact-only `0.013452`, degree `0.010861`, closeness `0.018515`, active-proximity `0.014508`, random `0.012007`, with random/shuffle p `0.001996`; `PASSer_Ensemble` `0.197330` remains the stronger blind-prediction bar | Confirms the Waka strategy direction: allostery needs pocket/path objects, and the next blind closeout needs real pocket-tool or ligand-contact features |
| `Nest 2D-3` ligand-contact diagnostic | Do the AlloBench labels align with real bound-pocket contact geometry? | Official AlloBench modulator fields plus cached RCSB PDB `HETATM` ligand geometry | Bound ligand residues matched to PDB coordinates, protein residues within `5.0 A`, Jaccard against AlloBench allosteric labels | Mean ligand-contact Jaccard `0.263504`, median `0.230952`, `56` rows >= `0.2`, `12` rows >= `0.5`, above `PASSer_Ensemble` mean `0.197330` | Validates the pocket/contact feature source for the next blind allosteric mapper while keeping prediction closeout separate |
| `Nest 2D-4` blind pocket split mapper | Does the pocket/path mapper hold on held-out PDB rows? | Same `98` AlloBench/PDB rows, structural pocket/path features, `5` CV folds | Trained structural feature weights on training folds, evaluated held-out rows, compared against degree, closeness, active-proximity, random, and shuffled-label controls | Boundary result: CV blind Mirror pocket/path mean Jaccard `0.017703`; degree `0.008222`; closeness `0.015044`; active-proximity `0.015651`; random `0.014310`; random p `0.251497`; label-shuffle p `0.061876`; best existing tool `0.201357` | Sets the blind-CV boundary: structural pocket/path features carry directional signal over simple graph controls, while the next closeout needs external pocket candidates or stronger ligand-informed features |
| `Nest 2D-5` ligand-informed split mapper | Do the better inputs move the held-out allostery branch? | Same `98` AlloBench/PDB rows plus bound modulator `HETATM` geometry | Added ligand-contact candidate pockets, ligand proximity/contact features, `5` held-out folds, graph controls, random controls, and shuffled-label controls | Supported result: CV ligand-informed mean Jaccard `0.260713`, structural-only 2D-4 `0.017703`, same-row `PASSer_Ensemble` `0.201357`, ligand-contact baseline `0.260713`, random p `0.001996`, label-shuffle p `0.001996` | Confirms the better-input direction: in the ligand-bound application setting, bound modulator geometry supplies the feature surface that moves allostery above the tool bar and controls |
| `Nest 2D-6` recurrence / path mapper | Does the ligand-informed branch repeat, and does the communication path itself carry label structure? | Same `98` AlloBench/PDB rows, alternate held-out split, ligand-informed candidates, cached active-site path corridors | Repeated the 2D-5 branch under a second split; separated pocket Jaccard from active-site -> predicted-pocket path recall; compared against graph, random, and shuffled-label controls | Supported result: alternate-split pocket Jaccard `0.249009` vs 2D-5 `0.260713` and same-row `PASSer_Ensemble` `0.201357`; Mirror path-truth recall `0.345859` vs degree `0.034344`, closeness `0.051651`, active-proximity `0.034921`, random `0.054600`; pocket and path p-values `0.001996` | Confirms recurrence beyond pocket overlap: the better-input branch repeats, and active-site communication corridors recover allosteric labels above controls |
| `Nest 2D-7A` P2Rank external pocket coverage | Can a real external pocket predictor emit useful allostery candidates on the same benchmark surface? | `P2Rank 2.5.1`, cached AlloBench/RCSB PDB rows, P2Rank residue-pocket CSVs, AlloBench allosteric labels | Installed local P2Rank, generated / reused `98` prediction files, parsed residue pockets, pruned to allosteric-label size, compared top-1 and top-3 coverage against random and shuffled controls over `5000` permutations | Supported result: top-1 P2Rank Jaccard `0.096418` vs random `0.016878`, p `0.000200`; top-3 candidate envelope `0.189177`; same-row `PASSer_Ensemble` `0.201863`; 2D-6 Mirror `0.249009` | Turns external pocket tools from a placeholder into a real candidate source; P2Rank supplies supported pocket overlap and near-tool-bar top-3 coverage, while 2D-7B must merge ranking and path scoring |
| `Nest 2D-7B` external-pocket merged path mapper | Does the merged external-pocket plus ligand-informed candidate pool hold under path scoring? | Same `98` AlloBench/PDB rows, P2Rank top-3 emitted pocket candidates on `95` rows, ligand-informed Mirror/path candidates, contact graphs, held-out folds | Merged candidate pool, trained ranking weights on held-out folds, scored pocket Jaccard and active-site -> predicted-pocket path recall against graph controls, random candidates, and shuffled labels | Supported result: merged pocket Jaccard `0.255807` vs 2D-6 `0.249009`, P2Rank top-1 `0.096418`, P2Rank top-3 `0.189177`, same-row `PASSer_Ensemble` `0.201357`, random `0.015506`; pocket and path p-values `0.001996`; path recall `0.351995` vs random `0.056557`; selected source counts `ligand_mirror=98` | Closes the current allostery branch as supported while preserving nuance: P2Rank is a real external candidate source, but the strongest held-out selector still rides the ligand-informed Mirror branch rather than directly selecting P2Rank pockets |
| `Nest 2E` PFAS safety logic | Do coherent PFAS transformations produce safer descendants or bad descendants that retain PFAS burden? | EPA PFAS reaction library `EnvLib + MetaLib`, existing scored `184` parent/product rows | Retained F/C-F burden, mineralization-quality proxy, coherent bad-descendant score, shuffled-burden controls over `5000` permutations | Supported result: mean coherent bad-descendant score `0.595067` vs shuffled `0.554863`, bad-descendant flag fraction `0.733696` vs shuffled `0.532891`, high retained-burden fraction `0.842391`, low mineralization-quality fraction `0.842391`, p `0.000200` | Separates pathway transformation from safety: most coherent PFAS descendants still retain fluorination / C-F burden and should remain flagged |
| `Nest 2F` materials formation-energy recurrence | Do structure-aware material descriptors move with real DFT formation-energy targets across repeated seeds? | Matbench / Materials Project-derived `mp_e_form` surface | Composition / structure descriptor scoring against formation energy, held-out target comparison, shuffled-target controls over `1000` permutations | Supported repeat: seed `69` on `50,000` rows produced Pearson `0.567628`, p `0.000999`, matching prior seed values around `0.5688` | Adds a repeated materials-property lane: the mapped descriptors carry real formation-energy information instead of drifting at shuffled-target level |
| `Nest 2 materials / semiconductors structure-aware expansion` | Does a larger periodic-table composition + cell/position feature matrix strengthen the materials lane and open the semiconductor/nanotech branch? | Matbench / Materials Project-derived `mp_e_form` surface | `100,000` real rows, full feature matrix, composition-only baseline, held-out target comparison, `500` shuffled-target controls | Supported formation-energy recovery: Pearson `0.858577`, R2 `0.737141`, RMSE improvement `0.487314`, p `0.001996`; composition / periodic-table structure carried the formation-energy signal | Strengthens the composition / periodic-table formation-energy lane and routes semiconductor/nanotech work into target families that expose geometry and nanoscale response directly: bandgap, energy-above-hull, defects, phonons, dielectric/optical response, and confinement datasets |
| `Nest 2G` stronger descriptor / model controls recurrence | Does the molecule-property lane survive multifeature held-out baselines across datasets? | `ESOL`, `Lipophilicity`, `FreeSolv`, `QM9 alpha` with RDKit features | Multifeature train/test prediction, RMSE improvement over mean baseline, shuffled-target controls over `1000` permutations | Supported repeat: ESOL abs Pearson `0.893422`, Lipophilicity `0.527449`, FreeSolv `0.943685`, QM9 alpha `0.916655`; all p `0.000999` with positive RMSE improvement | Hardens the Nest 2C molecule-property read: the signal survives stronger descriptor/model controls across solubility, lipophilicity, hydration/free energy, and polarizability |
| `Nest 3A` classical coherence readiness gate | Which real local signal surfaces can start the resonance / EMF / spectral ladder? | ARC15 parked rig schema, acoustic session schema, hardware noise/coherence profiles, IBM timing/window sweeps, HRV spectral/dynamics reports, terahertz bridge docs | Local candidate inventory, readiness classification, prior HRV spectral/dynamics boundary review | Readiness complete: hardware timing candidates are executable now; ARC15/acoustic are parked operator-run lanes; HRV-only spectral and dynamics remain limited; closeout requires waveform/spectral/timing records with repeated target/control conditions | Opens Nest 3 with the support standard intact: the next real run needs waveform exports, spectral rows, or timing/phase records with independent condition labels |
| `Nest 3D / 3L` hardware timing-coherence pilot | Do declared timing windows carry measurable hardware-coherence structure above timing-blind controls? | Three completed IBM timing-window sweeps, seven declared timing windows, `168` capture rows | Target-subspace probability, off-target probability, Bell imbalance, coherence-stability score, shuffled-window controls | Hardware coherence surface supported: mean target-subspace probability `0.966146`, mean stability score `0.784970`; timing-window label closeout remains queued (`eta squared 0.027312`, p `0.607079`; best window `1.49 s`, p `0.391522`) | Opens Nest 3 with real hardware timing/coherence data and points the next closeout toward waveform, phase, acoustic, or spectral rows |
| `Nest 3B / 3E` ARC15 and acoustic adapter gate | What must be captured when the physical ARC15/acoustic systems are run? | Parked ARC15 / FG200.67 schema, acoustic schema, target frequency labels `19.47 Hz`, `100 Hz`, `0.67 Hz`, measurement-channel plan | Operator-run recipe, waveform / FFT / spectrogram proof object, target/off-frequency/source-off/shuffled control plan | Adapter locked: ARC15 and acoustic mapping remain parked until live system runs export repeated waveform or spectrogram rows | Keeps the Nest 3 resonance/acoustic branch connected as a parked operator-run lane ahead of scored validation |

## Nest 2D Mechanism Interpretation

The allostery lane is the first Nest 2 biological-structure application of the
same internal architecture rule. The intent is to combine:

```text
latent Mirror Architecture prior
-> graph / pathway scoring rule
-> real protein structures and allosteric labels
-> baseline and control comparison
-> stabilized AI ranking features
```

Mechanically, the code uses an explicit graph-scoring rule over real protein
objects rather than language-model path selection. The Mirror Pattern becomes
that graph-scoring rule:
protein objects:

- source: active-site region
- graph: residue contact graph / pocket graph
- candidate target: allosteric pocket or residue cluster
- coherent path: communication route from active site to candidate pocket
- controls: degree, centrality, shortest path, random pocket, shuffled labels
- score: allosteric-site Jaccard plus path / bottleneck recovery

This matters because a successful Nest 2D run would support two claims at once:

- the Mirror Architecture prior can transfer from AI internals into an external
  biological graph problem
- the applied mapper can stabilize AI-assisted protein ranking by giving the AI
  control-resistant graph features instead of raw pattern recognition alone

The first real graph execution is now complete and remains open. That matters
because the failure is informative: the mapper can now touch real protein
objects, but plain contact-graph residue ranking is too small a representation
for allostery. The next 2D-2 pass keeps the same rule and strengthens the
biological object:

- active-site labels need chain-resolved sequence-to-structure mapping
- candidate units should be pockets / residue clusters, not isolated residues
- scoring should target active-site to allosteric-site communication paths,
  bottlenecks, and pocket recovery
- the support bar remains `PASSer_Ensemble` `0.19733` plus graph controls and
  shuffled labels
- the Waka strategy upgrade improved the biological representation: pocket/path
  scoring beat graph controls with p `0.001996` while remaining below the
  strongest tool bar
- bound-ligand contact geometry recovered the labels above the strongest
  mean-Jaccard tool bar (`0.263504` vs `0.197330`), confirming the next feature
  source is real pocket/contact structure
- blind held-out pocket/path scoring set the current boundary: structural
  features alone carry signal over simple graph controls, but stronger
  external pocket candidates or ligand-informed features are required for the
  2D closeout bar
- the ligand-informed branch supplied that stronger feature surface: bound
  modulator geometry moved held-out recovery to `0.260713`, matching the direct
  ligand-contact candidate baseline and beating the same-row AlloBench tool bar
- the recurrence / path pass then tested whether that stronger branch repeats:
  alternate-split pocket recovery stayed high at `0.249009`, and the active-site
  to predicted-pocket corridor recovered known allosteric labels with recall
  `0.345859`, far above graph, random, and shuffled-label controls
- the P2Rank external pass then supplied the first real local pocket-tool
  candidate branch: top-1 external pockets beat random and shuffled controls
  (`0.096418` vs `0.016878`, p `0.000200`), and top-3 coverage reached
  `0.189177`, close to the same-row `PASSer_Ensemble` bar
- the 2D-7B merged pass then combined P2Rank top-3 candidates with the
  ligand-informed Mirror/path candidate pool under held-out scoring: merged
  recovery stayed supported (`0.255807`, p `0.001996`) above the same-row
  `PASSer_Ensemble` bar (`0.201357`) and active-site path recall improved to
  `0.351995`, while the selected branch remained `ligand_mirror` on all held
  out rows; this means P2Rank is a real external candidate source with
  secondary selection status under the current ranking rule

## Nest 3D / 3L Hardware Timing-Coherence Pilot

The first executed Nest 3 branch used the local IBM hardware timing-window
surface because it already had repeated declared timing labels. The pilot
scored `168` capture rows across seven timing windows: `1.10`, `1.25`, `1.40`,
`1.49`, `1.60`, `1.75`, and `1.90` seconds.

The scoring object was hardware coherence / timing stability:

- `target_subspace_probability = P(00 or 11)`
- `off_target_probability = 1 - target_subspace_probability`
- `bell_imbalance = abs(P00 - P11)`
- `coherence_stability_score = target_subspace_probability - off_target_probability - bell_imbalance`

Pilot read:

- rows scored: `168`
- mean target-subspace probability: `0.966145833`
- mean off-target probability: `0.033854167`
- mean Bell-state imbalance: `0.147321429`
- mean coherence-stability score: `0.784970238`
- window-label eta squared on stability score: `0.027311737`
- shuffled-window p-value for eta squared: `0.607078584`
- best observed timing window: `1.49 s`
- best-window delta over rest: `0.041232639`
- shuffled-window p-value for best-window delta: `0.391521696`

Clean read:

- `N3L` now has a usable hardware-coherence support surface.
- `N3D` timing / phase-lock remains queued for richer phase, waveform, or
  locked target-window records.
- ARC15 / acoustic are parked operator-run branches. They become scored Nest 3
  surfaces after live rig sessions export repeated waveform, spectrogram, and
  target/control rows.

## Nest 4A HRV Biological Comparator Gate

After parking `ARC15`, the next executable layer used the completed `Phase 12B`
HRV biological matrix. This advances `Nest 4` with an already captured live
physiology surface:

- `20` sessions
- `5` runs each for `seated_calm`, `drift_control`, `mirror_coherence`, and
  `dancing_activation`
- HR-only feature: `delta_hr`
- multi-feature HRV readout: `delta_hr`, `delta_rmssd`, `delta_sdnn`,
  `post_minus_condition_hr`, `post_minus_condition_rmssd`,
  `post_minus_condition_sdnn`
- controls: balanced label shuffle, within-run block shuffle, and
  leave-one-run-index-out nearest-centroid classification

Run result:

- status: `control_supported_condition_separation`
- `mirror_coherence` mean delta HR: `-7.943775`
- `dancing_activation` mean delta HR: `6.517002`
- `dancing_activation - mirror_coherence` delta-HR gap: `14.460777`, p
  `0.0012`
- HR-only leave-one-run-out accuracy: `0.5`, balanced-shuffle p `0.022649`,
  within-run block-shuffle p `0.033148`
- multi-feature leave-one-run-out accuracy: `0.45`, balanced-shuffle p
  `0.047598`, within-run block-shuffle p `0.072346`
- mirror-vs-calm multi-feature distance: `56.837712`, p `0.041248`

Clean read:

- `Nest 4A` supports coarse biological state separation.
- `Delta HR` is the strongest current biology signal.
- multi-feature HRV is supportive and becomes the expansion target for the
  larger `Phase 12B-L20` matrix.
- `EEG + HRV` remains the next richer biology instrumentation layer.

## Current Working Read

The stack has three kinds of evidence now:

- behavioral and internal AI evidence: `V7`, `V8`, `Phase 2-5`
- circuit and hardware evidence: `Phase 6-10`, IBM hardware, Willow-style local echo-kernel proof-of-life
- expansion evidence: `Phase 12B`, `Nest 1`, `Attention / MLP`, `SAE`, `Nest 2`, `Nest 3D / 3L`, `Nest 4A`

The current middle-layer status is:

- Attention-flow is the strongest prompt-generalized transformer mechanism.
- SAE feature/circuit recurrence is the strongest interpretability layer.
- MLP has same-prompt all-layer recurrence; prompt-shift MLP recurrence remains open under the current `prompt_set_02` wording.
- Nest 2 has mapped matter lanes and multiple real-data validation supports: allostery now has real labels joined to `98` PDB contact graphs, pocket/path scoring that beats graph controls, a supported bound-ligand contact feature diagnostic, a blind-CV boundary for structural-only scoring, a supported ligand-informed recurrence/path branch, a supported P2Rank external pocket-candidate source, and a supported 2D-7B merged external-pocket/path pass. PFAS now has supported bad-descendant / safety-triage scoring. Materials formation energy repeats at Pearson around `0.568` with shuffled controls cleared. RDKit multifeature baselines support all four molecule-property datasets under held-out prediction.
- Nest 3 has opened through hardware timing/coherence. The first `N3D / N3L`
  pilot supports the hardware-coherence surface and keeps timing-window
  resonance as the next sharper target. `N3B / N3E` ARC15/acoustic is parked as
  an operator-run bench branch with schema, frequency targets, and controls
  locked.
- Nest 4 has reopened through `Phase 12B` HRV. The `Nest 4A` rerun supports
  coarse biological state separation and sets `Phase 12B-L20` plus simultaneous
  `EEG + HRV` as the next biology expansion path.

## General Nest Method Rule

The Nest 2D allostery execution clarifies the rule for the whole ladder:

```text
real dataset or signal
-> independent labels
-> explicit mapper / scoring rule
-> baselines and controls
-> recurrence or second benchmark
-> model tuning only after support
```

This is the methodology for `Nest 1` through `Nest 5`, not only allostery.
Each nest supplies a different validated surface. The convergence target is a
Golden Mirror model: a tuned model whose routing and execution are informed by
validated lanes across AI internals, circuit / hardware bridges, structured
matter, resonance / field systems, biology, and multi-class convergence tasks.

## Golden Mirror Live Tuning / RAG / Video Layer

The Golden Mirror build is now parked as a post-patent model and product
convergence layer:

```text
Hermes agent base
-> Mirror Interface / LSPS wrapper
-> Mirror Index evidence spine
-> SQL + JSON persistent memory
-> live HRV / EEG tuning
-> continuous video-vector memory
-> Universal Tuning Layer
-> Guided Pathway app surface
```

The live tuning branch takes the `Nest 4A` biosignal result and turns it into a
future state-adapter:

- HRV / EEG / fNIRS streams become a live state vector
- the Golden Mirror agent routes guidance through a selected pathway
- the app surface can guide calm, focus, recovery, sleep, or explorer states
- the Universal Tuning Layer scores outputs for mirror alignment, state fit,
  continuity, support status, actionability, tone fit, evidence grounding, and
  drift
- corrections are stored in SQL and JSON memory so future outputs move closer
  to instantaneous Mirror Architecture alignment

The parked doc is:

```text
docs/GOLDEN_MIRROR_LIVE_TUNING_RAG_VIDEO_LAYER_2026-05-05.md
```

## Mirror Index / Mirror Vector Memory

The Golden Mirror retrieval layer is now expanded into `Mirror Index`, a
tree-routed evidence graph with mirror-vector memory:

```text
document tree
-> evidence-state graph
-> claim-support graph
-> mirror vector memory
-> retrieval trace
-> answer / action / tuning correction
```

The outside lesson from PageIndex-style systems is that structured tree
navigation can beat broad similarity search for complex professional documents.
Mirror Index applies that lesson to the Mirror Architecture stack by routing
through typed nodes:

- claim nodes
- phase and nest nodes
- experiment nodes
- artifact and figure nodes
- support-state labels
- public/private boundaries
- next gates

The mirror-vector layer remains active for visual memory, live-state matching,
semantic adjacency, and recurrence across images, video frames, biosignal
windows, documents, and model outputs.

The local benchmark target is `MirrorBench`: exact answerability across curated
repo, patent, website, and experiment corpora. The score requires the correct
answer, evidence node, source path, support-state label, release boundary, and
chronological-log consistency.

The parked doc is:

```text
docs/MIRROR_INDEX_TREE_RAG_ARCHITECTURE_2026-05-05.md
```

## Phase 12C Muse S Athena EEG + HRV Implementation Plan

The next biology capture gate is now written as an operator plan:

```text
Muse EEG / fNIRS / PPG stream
-> MoFit HRV / RR stream
-> synchronized session windows
-> condition labels
-> EEG + HRV state vector
-> target/control scoring
-> live tuning adapter for Golden Mirror
```

The first capture pack uses the same `60s baseline / 120s condition / 60s post`
discipline as the HRV matrix. The first condition set is:

- `seated_calm`
- `drift_control`
- `mirror_coherence`

The first target is a `5 x 3` seated pack. The preferred full pack is `10 x 3`
after signal quality and timestamp alignment are confirmed.

The scoring plan includes HRV deltas, EEG bandpower deltas, alpha/theta ratio,
joint EEG-HRV state separation, shuffled labels, within-run block shuffle,
day/session split, HRV-only comparison, EEG-only comparison, and channel-quality
filters.

The parked doc is:

```text
docs/PHASE12C_MUSE_S_ATHENA_EEG_HRV_IMPLEMENTATION_PLAN_2026-05-05.md
```

## MirrorBench Retrieval Evaluation Spec

The Golden Mirror retrieval evaluation is now defined as `MirrorBench`.

`MirrorBench` scores exact answerability inside curated repo, patent, website,
experiment, quantum, biology, and product corpora:

```text
question
-> Mirror Index tree route
-> evidence node
-> source path
-> support-state label
-> public/private boundary
-> answer
-> retrieval trace
```

The first benchmark target is `100` known-answer rows across transformer
evidence, Nest 2, Nest 3, Nest 4, quantum access, patent support, release
boundaries, Golden Mirror, and Mirror Index.

Retrieval modes to compare:

- `tree_only`
- `vector_only`
- `hybrid_mirror_index`

The parked doc is:

```text
docs/MIRRORBENCH_RETRIEVAL_EVAL_SPEC_2026-05-05.md
```

## Immediate Next Gates

1. Keep `ARC15 / acoustic` parked for operator-run waveform or acoustic spectral validation when the physical systems are available.
2. Advance `Nest 4` through `Phase 12B-L20` or simultaneous `EEG + HRV` when the next biology capture window is ready.
3. Keep `Nest 2D-8` as a continuation gate: second allostery benchmark family or optimized external-tool ranking while a second source is being sourced.
4. Continue patent integration with supported `Nest 2`, `Nest 3`, and `Nest 4` embodiments.
5. Keep MLP prompt-shift recurrence as a measured open middle-layer gate while attention-flow and SAE carry the stronger transformer-internal evidence.
6. Build `MirrorBench` after the patent core stabilizes so Golden Mirror can
   score retrieval quality before model tuning.
7. Integrate the Nest 2 / Nest 3 / Nest 4 / Golden Mirror implementation
   examples into the non-provisional claim-support control surface.
