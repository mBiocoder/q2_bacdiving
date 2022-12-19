# q2_bacdiving

q2-bacdiving is a [Qiime2](https://qiime2.org/) plugin that accesses and retrieves information from the world's largest database for standardized bacterial phenotypic information: BacDive. It implements [Bacdiving's](https://github.com/mBiocoder/Bacdiving) core function bacdive_call(). 

Before using q2-bacdiving please register (for free) on [BacDive](https://api.bacdive.dsmz.de/) and make sure you have [qiime](https://docs.qiime2.org/2022.8/install/native/#install-qiime-2-within-a-conda-environment) installed.

In general, q2-bacdiving can deal with two types of input data: a taxonomy table (e.g. as extracted from a phyloseq-object) or an input file (.csv, .txt, .tsv) with one query-type per row. Possible BacDive query types include: BacDive id, taxonomy (as in species name), 16S sequencing accession id (e.g. SILVA id), culture collection accession id or genome sequence accession id.
However, the input file should be consistant with only contain one (!) query type for all of its rows.

Here is a minimal example on how to use q2-bacdiving, please refer to the full [documentation](https://bacdiving.readthedocs.io/en/latest/) for more details:

```
# File input type
```
