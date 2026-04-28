---
configs:
- config_name: default
  data_files: "co/*.parquet"
- config_name: info
  data_files: "ds.parquet"
license: mit
tags:
- molecular dynamics
- mlip
- interatomic potential
pretty_name: Matbench mp e form
---
### <details><summary>Cite this dataset </summary>Dunn, A., Wang, Q., Ganose, A., Dopp, D., and Jain, A. _Matbench mp e form_. ColabFit, 2024. https://doi.org/10.60732/3cef7b09</details>
#### This dataset has been curated and formatted for the ColabFit Exchange
#### This dataset is also available on the ColabFit Exchange:
https://materials.colabfit.org/id/DS_5drebe4tktiu_0
#### Visit the ColabFit Exchange to search additional datasets by author, description, element content and more.
https://materials.colabfit.org
<br><hr>
# Dataset  Name
Matbench mp e form
### Description
Matbench v0.1 test dataset for predicting DFT formation energy from structure. Adapted from Materials Project database. Entries having formation energy more than 2.5eV and those containing noble gases are removed. Retrieved April 2, 2019. For benchmarking w/ nested cross validation, the order of the dataset must be identical to the retrieved data; refer to the Automatminer/Matbench publication for more details.Matbench is an automated leaderboard for benchmarking state of the art ML algorithms predicting a diverse range of solid materials' properties. It is hosted and maintained by the Materials Project.
### Dataset authors
Alexander Dunn, Qi Wang, Alex Ganose, Daniel Dopp, Anubhav Jain
### Publication
https://doi.org/10.1038/s41524-020-00406-3
### Original data link
https://matbench.materialsproject.org/
### License
MIT
### Number of unique molecular configurations
132741
### Number of atoms
3869238
### Elements included
Ac, Ag, Al, As, Au, B, Ba, Be, Bi, Br, C, Ca, Cd, Ce, Cl, Co, Cr, Cs, Cu, Dy, Er, Eu, F, Fe, Ga, Gd, Ge, H, Hf, Hg, Ho, I, In, Ir, K, La, Li, Lu, Mg, Mn, Mo, N, Na, Nb, Nd, Ni, Np, O, Os, P, Pa, Pb, Pd, Pm, Pr, Pt, Pu, Rb, Re, Rh, Ru, S, Sb, Sc, Se, Si, Sm, Sn, Sr, Ta, Tb, Tc, Te, Th, Ti, Tl, Tm, U, V, W, Y, Yb, Zn, Zr
### Properties included
formation energy
<br>
<hr>

# Usage
- `ds.parquet` : Aggregated dataset information.
- `co/` directory: Configuration rows each include a structure, calculated properties, and metadata.
- `cs/` directory : Configuration sets are subsets of configurations grouped by some common characteristic. If `cs/` does not exist, no configurations sets have been defined for this dataset.
- `cs_co_map/` directory : The mapping of configurations to configuration sets (if defined).
<br>
#### ColabFit Exchange documentation includes descriptions of content and example code for parsing parquet files:
- [Parquet parsing: example code](https://materials.colabfit.org/docs/how_to_use_parquet)
- [Dataset info schema](https://materials.colabfit.org/docs/dataset_schema)
- [Configuration schema](https://materials.colabfit.org/docs/configuration_schema)
- [Configuration set schema](https://materials.colabfit.org/docs/configuration_set_schema)
- [Configuration set to configuration mapping schema](https://materials.colabfit.org/docs/cs_co_mapping_schema)
