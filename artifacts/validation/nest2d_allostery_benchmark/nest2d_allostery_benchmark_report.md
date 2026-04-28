# Nest 2D Allostery Benchmark Extraction Report

Status: `completed_real_allostery_benchmark_extracted_mapper_not_scored`

## Inputs

- Source: AlloBench supporting-information PDF
- Article: `AlloBench: A Data
Set Pipeline for the Development
and Benchmarking of Allosteric Site Prediction Tools`
- DOI: `10.1021/acsomega.5c01263.s001`
- Extracted table: Table S3, topmost allosteric-site prediction Jaccard index

## Result

- extracted PDB rows: `100`
- prediction-tool columns: `10`
- best mean Jaccard tool in extracted table: `PASSer_Ensemble`
- best mean Jaccard: `0.197330`

## Clean Read

This is a real allostery benchmark surface, not a toy table.

It does not yet validate the Mirror mapper because the current extracted
table reports existing tool Jaccard scores. To score our own pathway
mapper, the next input must be a residue/contact graph plus known
allosteric-site residue labels or pocket membership labels.

## Next Missing Input

- protein contact graph or pocket graph per PDB row
- known allosteric-site residue / pocket labels
- mapper score for candidate communication path
- controls against degree / centrality / shuffled-site labels
