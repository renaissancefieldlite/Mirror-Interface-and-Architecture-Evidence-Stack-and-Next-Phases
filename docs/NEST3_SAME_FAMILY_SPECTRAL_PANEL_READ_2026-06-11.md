# Nest 3 Same-Family Spectral Panel Read

Date: `2026-06-11`

Run ID: `nest3_same_family_spectral_panel_2026-06-11`

Status: `real_data / public_spectral_sources / same_family_stress_panel / mixed_candidate_support`

## Gate State

Primary requested gate: a real Terahertz exposure-response dataset with
sham/off-window/heat-matched controls, or local/partner source-on/source-off
instrument rows.

Primary gate result: not seated in this run. The public literature has useful
THz exposure-response anchors, including the `2023` Scientific Reports melanoma
THz demethylation paper and its supplement, but the inspected supplement gives
a KEGG/GSEA pathway table rather than raw sample-level sham, heat-matched, or
off-window rows. That makes it a literature anchor, not a clean public
exposure-response dataset for this gate.

Backup gate executed: expanded same-family `IR / Raman / THz` panel using real
public spectral sources already seated in the evidence stack.

## Sources

| Source | Use in this run | Public URL |
| --- | --- | --- |
| NIST Chemistry WebBook gas-phase infrared spectra | same-family IR controls | https://webbook.nist.gov/chemistry/ |
| NIST Chemistry WebBook THz Spectral Database | same-family THz controls | https://webbook.nist.gov/chemistry/thz-ir/ |
| NASA Ames Ramdb Raman Spectroscopic Database | same-project Raman controls | https://www.astrochemistry.org/ramdb/ |
| Scientific Reports THz melanoma study | literature anchor only; no raw control matrix seated | https://www.nature.com/articles/s41598-023-31828-w |


## Explanatory Read

This gate keeps the arc honest. The goal was to find a real Terahertz
exposure-response dataset where a source is turned on, compared against sham or
heat-matched controls, and measured as a biological or material response. That
clean public dataset did not seat. The available THz biology paper is useful,
but its supplement gives pathway-level results rather than the raw controlled
rows needed for our evidence standard.

So the lane moved to the backup question: if we cannot yet prove
source-on/source-off exposure response, can we still show that real spectra carry
structured state information when easy category separation is removed? The
same-family panel does that. Instead of comparing unrelated materials, it asks
nearby questions: ketone versus aldehyde, aromatic hydrocarbon versus alkane,
sugar versus starch, salt/carbonate versus silicate/clay, and complex amino acids
versus simple amino acids.

The answer is mixed but useful. Some rows stay above shuffled controls; some
collapse; some remain high under nuisance controls, which means the model may be
reading broad curve shape instead of a deeper phase or exposure pattern. That is
not failure. It tells us exactly where the next proof has to go: real
source-on/source-off rows, stronger external holdouts, and raw exposure-response
measurements.

In plain terms: this pass strengthens the physical spectra layer, but it does
not close the THz biological bridge. The bridge is still open, and now the next
required evidence is clearer.

## Control Design

The point of this pass is to remove easy broad-family separation where possible.
Rows are tested inside nearby chemical or spectral families:

- `IR carbonyl`: ketones vs aldehydes.
- `IR hydrocarbon`: aromatics vs alkanes.
- `IR oxygenated`: alcohols vs carbonyl compounds.
- `THz carbohydrate`: simple sugars vs starch/cellulose.
- `THz inorganic`: salts/carbonates vs silicates/clays.
- `Raman amino acid`: complex/aromatic/acidic amino acids vs smaller/simple
  amino acids inside the same NASA Ames Ramdb project.

Controls include shuffled labels, band-position shuffle for spectral-position
dependence, distribution-only scoring, feature shuffle, and group-label
shuffle for the Raman row.

## Results

| Lane | Row | Status | Records | Observed AUC | Shuffled/control AUC | Control p | Band-position shuffle AUC | Distribution-only AUC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NIST gas IR | IR carbonyl ketone vs aldehyde | `weak_or_null` | `8` (`5` / `3`) | `0.666667` | `0.500667` | `0.338308` | `0.533333` | `0.800000` |
| NIST gas IR | IR hydrocarbon aromatic vs alkane | `partial_support` | `12` (`6` / `6`) | `0.805556` | `0.442083` | `0.069652` | `0.333333` | `0.833333` |
| NIST gas IR | IR oxygenated alcohol vs carbonyl | `candidate` | `14` (`6` / `8`) | `0.770833` | `0.472187` | `0.089552` | `0.312500` | `0.520833` |
| NIST THz | THz carbohydrate simple sugars vs starch/cellulose | `partial_support` | `10` (`7` / `3`) | `1.000000` | `0.483810` | `0.034826` | `0.857143` | `0.857143` |
| NIST THz | THz inorganic salt/carbonate vs silicate/clay | `candidate` | `9` (`4` / `5`) | `0.850000` | `0.499500` | `0.109453` | `0.100000` | `0.400000` |
| NASA Ames Ramdb Raman | Raman amino acid internal complex/aromatic/acidic vs simple | `candidate` | `24` (`9` / `15`) | `0.703704` | `0.512778` | `0.179104` | `0.666667` | `n/a` |

## Support Read

The same-family stress panel is a mixed support read, which is the correct
answer for this harder gate:

- The `THz carbohydrate simple sugars vs starch/cellulose` row gives the
  strongest internal THz signal: observed AUC `1.000000` against shuffled-label
  mean AUC near chance. Because band-position and distribution-only controls
  also remain high, this is candidate/partial support for THz material-state
  structure, not exposure-response closeout.
- The `IR hydrocarbon` and `IR oxygenated` rows keep above-chance same-family
  signal, but do not fully clear all nuisance controls.
- The `THz inorganic` row holds above-chance signal and collapses under
  band-position shuffle, but label-shuffle p value is not strong enough for a
  hard support call.
- The `Raman amino acid` row is candidate support only. It is useful because it
  stays inside one project and uses compound-level group controls, but it does
  not yet close the within-family Raman lane.

## Boundary

This is not a biological THz exposure-response result. It is not a medical THz
tuning claim, not a cellular response claim, and not a source-on/source-off
instrument row. It strengthens the public spectral-source scaffold while keeping
the true exposure-response gate open.

## Next Gate

To close the Terahertz bridge cleanly, the next run still needs one of:

1. a real sample-level THz exposure-response dataset with sham, heat-matched,
   off-window, and frequency-condition controls;
2. local/partner source-on/source-off instrument rows with matched baseline,
   distance, duration, power, frequency, and temperature logging;
3. a larger same-family raw spectra panel with external holdouts and stronger
   nuisance controls.
