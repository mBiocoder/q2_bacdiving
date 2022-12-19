# q2_bacdiving

q2-bacdiving is a [Qiime2](https://qiime2.org/) plugin that accesses and retrieves information from the world's largest database for standardized bacterial phenotypic information: BacDive. It implements [Bacdiving's](https://github.com/mBiocoder/Bacdiving) core function bacdive_call(). 

Before using q2-bacdiving please register (for free) on [BacDive](https://api.bacdive.dsmz.de/) and make sure you have [qiime](https://docs.qiime2.org/2022.8/install/native/#install-qiime-2-within-a-conda-environment) installed.

In general, q2-bacdiving can deal with two types of input data: a taxonomy table (e.g. as extracted from a phyloseq-object) or an input file (.csv, .txt, .tsv) with one query-type per row. Possible BacDive query types include: BacDive id, taxonomy (as in species name), 16S sequencing accession id (e.g. SILVA id), culture collection accession id or genome sequence accession id.
However, the input file should be consistant with only contain one (!) query type for all of its rows.

Here is a minimal example on how to use q2-bacdiving, please refer to the full [documentation](https://bacdiving.readthedocs.io/en/latest/) for more details:

```
# File input (SILVA ids)
qiime bacdiving bacdive-call --p-bacdive-id "<your-id>" --p-bacdive-password "<your-pw>" --p-input-via-file True --p-input-file-path "./SILVA_ids.txt" --p-sample-name "Sample1" --p-search-by-seq-accession True --p-print-res-df-to-file True --p-print-access-stats True --o-visualization "./final1.qzv"
```

```
# Taxonomy table input
qiime bacdiving bacdive-call --p-bacdive-id "<your-id>" --p-bacdive-password "<your-pw>" --p-taxtable-input True --p-taxtable-file-path "./lopresti_taxtab.tsv" --p-sample-name "lopresti" --p-print-res-df-to-file True --p-print-access-stats True --p-print-flattened-file True --o-visualization "./final2.qzv"
```

Depending on how big your input files are, you may need to wait a little before your output files are saved.
