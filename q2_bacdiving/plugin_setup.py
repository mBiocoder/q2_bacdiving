#!/usr/bin/env python3
import sys
from os.path import dirname

import qiime2.core.type.collection

# make sure you are in the correct directory
# q2_bacdiving_dir = dirname(os.getcwd())
q2_bacdiving_dir = dirname('/opt/project/')
sys.path.append(q2_bacdiving_dir)

import q2_bacdiving as q2b


from qiime2.plugin import (Plugin, Str, List, Int, Bool)

plugin = Plugin(
    name="bacdiving",
    version=q2b.__version__,
    website="https://github.com/mBiocoder/q2_bacdiving/",
    package="q2-bacdiving",
    short_description=(
        "Package for accessing and visualizing data from BacDive database"
    ),
    description=("q2-bacdiving accesses and retrieves information from the world's largest database for standardized bacterial phenotypic information: BacDive. If you have not registered for Bacdive web services yet, please do so using the following link before running this package: https://api.bacdive.dsmz.de/"),
)

plugin.visualizers.register_function(
    function= q2b.bacdive_call,
    inputs={},
    input_descriptions={},
    parameters={"bacdive_id": Str, "bacdive_password": Str, "input_via_file": Bool, "input_file_path": Str, "search_by_id": Bool, "search_by_culture_collection": Bool, "search_by_taxonomy": Bool, "search_by_seq_accession" : Bool, "search_by_genome_accession": Bool, "taxtable_input": Bool, "taxtable_file_path": Str, "sample_name": Str, "print_res_df_to_file": Bool, "print_access_stats": Bool, "print_flattened_file": Bool},
    parameter_descriptions={
        "bacdive_id": (
            "Log-in credential: BacDive id. Either bacdive_id and bacdive_pw can be set as function parameters or if left as empty strings, users will be prompted to input credentials."
        ),
        "bacdive_password": (
            "Log-in credential: BacDive password. Either bacdive_id and bacdive_pw can be set as function parameters or if left as empty strings, users will be prompted to input credentials."
        ),
        "input_via_file": (
            "If input is a file (.csv, .tsv, or .txt) with one entry per row, then set input_via_file = True."
        ),
        "input_file_path": (
            "If input_via_file = True, specify the input file path."
        ),
        "search_by_id": (
            "If input_via_file = True and the content of the input file are BacDive ids, set search_by_id = True."
        ),
        "search_by_culture_collection": (
            "If input_via_file = True and the content of the input file are culture collection ids, set search_by_culture_collection = True."
        ),
        "search_by_taxonomy": (
            "If input_via_file = True and the content of the input file are species, set search_by_taxonomy = True."
        ),
        "search_by_seq_accession": (
            "If input_via_file = True and the content of the input file are 16S sequence accession ids (e.g. SILVA ids), set search_by_16S_seq_accession = True."
        ),
        "search_by_genome_accession": (
            "If input_via_file = True and the content of the input file are genome accession ids, set search_by_genome_accession = True."
        ),
        "taxtable_input": (
            "If input is a taxonomy table (e.g. extracted from phyloseq-object), then set taxtable_input = True."
        ),
        "taxtable_file_path": (
            "If taxtable_input = True, specify the taxtable file path."
        ),
        "sample_name": (
            "Sample name."
        ),
        "print_res_df_to_file": (
            "If the resulting dataframe should be printed to file (as BacdiveInformation.tsv), then set to True."
        ),
        "print_access_stats": (
            "If the resulting BacDive access statistics should be printed to file, then set print_access_stats = True."
        ),
        "print_flattened_file": (
            "If the flattened BacDive information should be printed to file, then set print_flattened_file = True."
        ),
    },
    name='BacDive access and retrieval of information',
    description=("For single input file this function reads the input, queries the BacDive database and stores resulting dataframe(s) and access statistics.")
)
