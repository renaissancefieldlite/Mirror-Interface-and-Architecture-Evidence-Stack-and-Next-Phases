# GlyTouCan Glycan Source Confirmation Read

Date: `2026-05-27`

Run ID: `nest4_glytoucan_human_mouse_glycan_gate_2026-05-27`

Status: `real_data / GlyTouCan_GlyCosmos_RDF / glycan_source_candidate_support / HMDB_open`

## Source

Dataset: GlyTouCan / GlyCosmos RDF query through the public SPARQL endpoint.

GlyTouCan: https://glytoucan.org/

SPARQL endpoint: https://ts.glycosmos.org/sparql

Local query:

```text
private-local query: experiments/nest4_glytoucan_glycan_confirmation/data/raw/glytoucan_human_mouse_iupac_query.rq
```

Local source table:

```text
private-local source table: experiments/nest4_glytoucan_glycan_confirmation/data/raw/glytoucan_human_mouse_iupac.csv
```

Rows:

- raw rows: `3739`
- cleaned rows: `3739`
- balanced rows used: `1026`
- target rows: `513`
- control rows: `513`
- features used: `44`

Target/control:

```text
human source glycans / taxon 9606 vs mouse source glycans / taxon 10090
```

Source labels are not included in the feature matrix.

## Universal Data Pattern Packet

| Field | Read |
| --- | --- |
| `source` | GlyTouCan/GlyCosmos RDF glycan rows |
| `state` | human source glycans, taxon 9606 |
| `control` | mouse source glycans, taxon 10090, shuffled labels, feature shuffle |
| `transform` | IUPAC sequence length, branch counts, monosaccharide counts, linkage counts, sequence ratios |
| `invariant` | source-labeled glycan rows should preserve separable sequence-structure statistics if the source pattern is real |
| `drift` | source imbalance, species overlap, incomplete glycans, sequence-format variation |
| `score` | ROC-AUC, average precision, balanced accuracy, permutation p-value |
| `failure mode` | observed score near shuffled/control AUC or only length-only structure surviving |

## Results

| Metric | Observed | Shuffled-label control | Feature-shuffle control | Length/branch-only control |
| --- | ---: | ---: | ---: | ---: |
| `ROC-AUC mean` | `0.739219` | `0.499838` | `0.525007` | `0.563272` |
| `Average precision mean` | `0.782487` | `not repeated` | `0.525179` | `0.579031` |
| `Balanced accuracy mean` | `0.671378` | `not repeated` | `0.528327` | `0.538921` |
| `F1 mean` | `0.648355` | `not repeated` | `0.535607` | `0.517190` |
| `Permutation p-value` | `0.009901` | `100 repeats` | `n/a` | `n/a` |

## Top Feature Effects

| Feature | target minus control mean | effect size |
| --- | ---: | ---: |
| `link_b1-6` | `0.267057` | `0.624382` |
| `link_b1-3` | `0.475634` | `0.543372` |
| `mono_Gal` | `0.656920` | `0.450827` |
| `mono_GalNAc` | `0.216374` | `0.401682` |
| `ol_tail` | `0.148148` | `0.377381` |
| `mono_Fuc` | `0.269006` | `0.340385` |
| `fucose_total` | `0.269006` | `0.340385` |
| `fucose_per_mono` | `0.024245` | `0.326746` |
| `mono_Man` | `-0.643275` | `-0.322177` |
| `mono_Neu5Gc` | `-0.079922` | `-0.303474` |
| `terminal_dash` | `-0.126706` | `-0.256895` |
| `link_a1-6` | `-0.212476` | `-0.247126` |

## Support Read

This gives Nest 4 a separate glycan-source row from GlyTouCan/GlyCosmos. It
does not reuse ChEBI or LIPID MAPS labels. The read is conservative: it says
human-vs-mouse source-labeled glycan sequence rows show candidate support under
UDP controls, not that a clinical glycan result is complete.

Public-safe wording:

```text
GlyTouCan/GlyCosmos source gate completed. Human and mouse source-labeled glycan
sequence rows show candidate support under shuffled-label and feature-shuffle
controls, adding an independent glycan branch to the Nest 4 biomolecular lane.
```

## Boundary

This is not HMDB metabolomics, not a disease-marker claim, not clinical
glycomics, not nutrition/treatment guidance, and not paired HRV/Muse/Thermo
physiology.

## Next Gate

Run:

```text
HMDB access/download check
```

Then:

```text
HRV + Muse + Thermo paired physiology manifest
```
