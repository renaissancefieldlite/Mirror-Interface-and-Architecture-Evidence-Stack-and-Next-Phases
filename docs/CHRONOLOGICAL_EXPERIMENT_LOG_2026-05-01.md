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

Mechanically, the code should not ask a language model to choose the protein
path. The Mirror Pattern becomes an explicit graph-scoring rule over real
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

## Current Working Read

The stack has three kinds of evidence now:

- behavioral and internal AI evidence: `V7`, `V8`, `Phase 2-5`
- circuit and hardware evidence: `Phase 6-10`, IBM hardware, Willow-style local echo-kernel proof-of-life
- expansion evidence: `Phase 12B`, `Nest 1`, `Attention / MLP`, `SAE`, `Nest 2`

The current middle-layer status is:

- Attention-flow is the strongest prompt-generalized transformer mechanism.
- SAE feature/circuit recurrence is the strongest interpretability layer.
- MLP has same-prompt all-layer recurrence; prompt-shift MLP recurrence remains open under the current `prompt_set_02` wording.
- Nest 2 has mapped matter lanes and started real-data validation; allostery now has real labels joined to `98` PDB contact graphs, pocket/path scoring that beats graph controls, and a supported bound-ligand contact feature diagnostic.

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

## Immediate Next Gates

1. Run the `Nest 2D-4` blind mapper upgrade: external pocket-tool candidates or local ligand-informed pocket features, communication-path scoring, and the same AlloBench / graph-control bar.
2. Continue `Nest 2E` PFAS safety logic, `Nest 2F` materials structure-aware baselines, and `Nest 2G` descriptor / model controls.
3. Keep MLP prompt-shift recurrence as a measured open middle-layer gate while attention-flow and SAE carry the stronger transformer-internal evidence.
