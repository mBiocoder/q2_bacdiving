#!/usr/bin/python3
import contextlib
import csv
import os

import bacdive
import pandas as pd
import pandas.errors
from pylab import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from alive_progress import alive_bar

from typing import List, Set, Dict, Tuple
#import q2templates

import jinja2
from bokeh.embed import components
from bokeh.resources import INLINE

import pkg_resources
TEMPLATES = pkg_resources.resource_filename('q2_bacdiving._bacdiveInformation', 'assets')


def bacdive_call(output_dir: str ="./", bacdive_id: str ="", bacdive_password: str ="", input_via_file: bool = False, input_file_path: str =" ", search_by_id: bool = False, search_by_culture_collection: bool = False, search_by_taxonomy: bool = False, search_by_seq_accession: bool = False, search_by_genome_accession : bool = False, taxtable_input: bool = False, taxtable_file_path: str = " ", sample_name: str = "", print_res_df_to_file: bool = True, print_access_stats: bool = True, print_flattened_file: bool = False) -> None:
    try:
        if input_via_file == True and taxtable_input == False:
            dfs = []
            client = bacdive.BacdiveClient(bacdive_id, bacdive_password)  # Access Bacdive

            total_number_silva_ids_input = 0
            access_failed = 0
            not_found = []

            # Reading in all SILVA ids and running query in Bacdive
            with open(input_file_path) as file:
                txt_file = csv.reader(file, delimiter="\t")
                with alive_bar(force_tty=True) as bar:
                    for line in txt_file:
                        query_id = "".join(line)
                        total_number_silva_ids_input += 1

                        bar()
                        # Search Bacdive in various ways:
                        if search_by_seq_accession == True and search_by_id == False and search_by_culture_collection == False and search_by_taxonomy == False and search_by_genome_accession == False:
                            query = {"16s": query_id}
                        elif search_by_taxonomy == True and search_by_genome_accession == False and search_by_seq_accession == False and search_by_id == False and search_by_culture_collection == False:
                            query = {"taxonomy": query_id}
                        elif search_by_genome_accession == True and search_by_seq_accession == False and search_by_id == False and search_by_culture_collection == False and search_by_taxonomy == False:
                            query = {"genome": query_id}
                        elif search_by_id == True and search_by_culture_collection == False and search_by_taxonomy == False and search_by_genome_accession == False and search_by_seq_accession == False:
                            query = {"id": query_id}
                        elif search_by_culture_collection == True and search_by_taxonomy == False and search_by_genome_accession == False and search_by_seq_accession == False and search_by_id == False:
                            query = {"culturecolno": query_id}
                        else:
                            print("Please make sure your parameters for your input file are correct.")
                            exit(1)
                        # run query
                        try:
                            with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
                                result = client.search(**query)
                                for strain in client.retrieve():
                                    tmp = pd.json_normalize(strain)
                                    df = pd.DataFrame.from_dict(tmp)
                                    dfs.append(df)  # append the data frame to the list
                        except KeyError:
                            access_failed += 1
                            not_found.append(query_id)

            # Create resulting dataframe
            resulting_df = pd.concat(dfs, ignore_index=True)  # concatenate all the data frames in the list

            with open(os.path.join(output_dir, 'index.tsv'), 'w') as fh:
                fh.write("This is the index file.")
            fh.close()

            # Bacdive access statistics
            if print_access_stats == True:
                # Prints access statistics for input file types
                access_worked = total_number_silva_ids_input - access_failed
                percentage_found = access_worked / total_number_silva_ids_input * 100
                file = open(os.path.join(output_dir, '%s access_stats_SILVA_input.tsv' % sample_name), "w")
                file.write("-- Access statistics --" + "\n")
                file.write("-> Total number of SILVA ids are: " + str(total_number_silva_ids_input) + ", out of which " + str(round(percentage_found, 2)) + "% were found on Bacdive. Therefore, " + str(access_failed) + " SILVA ids were not found in Bacdive." + "\n")
                file.write("The following SILVA ids were not found on Bacdive: " + "\n")
                for i in not_found:
                    file.write(i + "\n")
                file.close()

            if print_res_df_to_file == True:
                # Writes resulting dataframe with all BacDive information to file
                with open(os.path.join(output_dir, '%s BacdiveInformation.tsv' % sample_name), 'w') as fw:
                    fw.write(resulting_df.to_csv(sep='\t', encoding='utf-8', index=True))
                fw.close()

        elif taxtable_input == True and input_via_file == False:

            dfs = []
            client = bacdive.BacdiveClient(bacdive_id, bacdive_password)

            access_failed = 0
            not_found = []

            final_df = pd.read_table(taxtable_file_path, index_col=0)

            # Select rows which do not have NaN value in column 'Species'
            selected_rows = final_df[~final_df['Species'].isnull()]
            # Merge values from Genus and Species column for Bacdive query
            df_new = selected_rows.Genus.str.cat(selected_rows.Species, sep=' ')
            # Write resulting species found from input file to an output file
            with open(os.path.join(output_dir, '%s_Species_names_from_taxtable_file.csv' % sample_name), 'w') as fl:
                fl.write(df_new.to_csv(index=False,header=None))
            fl.close()

            # read output file and return this dataframe
            try:
                downstream_df = pd.read_csv(output_dir + "/%s_Species_names_from_taxtable_file.csv" %sample_name, header=None)
            except pandas.errors.EmptyDataError:
                print("There are no species information available for this dataset!")
                sys.exit(0)

            total_number_species_input = downstream_df[downstream_df.columns[0]].count()

            with alive_bar(force_tty=True, total=int(total_number_species_input)) as bar:
                for species in downstream_df[0]:
                    bar()
                    # run query
                    try:
                        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
                            result = client.search(taxonomy=species)
                        for strain in client.retrieve():
                            tmp = pd.json_normalize(strain)
                            df = pd.DataFrame.from_dict(tmp)
                            dfs.append(df)  # append the data frame to the list
                    except KeyError:
                        access_failed += 1
                        not_found.append(species)

                resulting_df = pd.concat(dfs, ignore_index=True)  # concatenate all the data frames in the list

                # Bacdive access statistics
                if print_access_stats == True:
                    # Prints access statistics for input taxonomy tables
                    access_worked = total_number_species_input - access_failed
                    percentage_found = access_worked / total_number_species_input * 100
                    file = open(os.path.join(output_dir, '%s access_stats_taxtable_input.tsv' % sample_name), "w")
                    file.write("-- Access statistics --" + "\n")
                    file.write("-> Your input taxtable file contains " + str(
                        len(final_df)) + " rows. After removing NaN species-values from the dataframe we are left with " + str(
                        len(selected_rows)) + " rows." + "\n")
                    file.write("-> Total number of rows are: " + str(total_number_species_input) + ", out of which " + str(round(percentage_found, 2)) + "% were found on Bacdive. Therefore, " + str(access_failed) + " species were not found in Bacdive." + "\n")
                    file.write("\n")
                    file.write("The following species were not found on Bacdive: " + "\n")
                    for i in not_found:
                        file.write(i + "\n")
                    file.close()

                if print_res_df_to_file == True:
                    # Writes resulting dataframe with all BacDive information to file
                    with open(os.path.join(output_dir, '%s BacdiveInformation.tsv' % sample_name), 'w') as fw:
                        fw.write(resulting_df.to_csv(sep='\t', encoding='utf-8', index=True))
                    fw.close()

                if print_flattened_file == True:
                    columns_of_interest = ["Physiology and metabolism.oxygen tolerance.oxygen tolerance", "Morphology.cell morphology.motility", "Culture and growth conditions.culture temp.growth", "Name and taxonomic classification.type strain", "Culture and growth conditions.culture temp.temperature", "Culture and growth conditions.culture temp.range", "Isolation, sampling and environmental information.isolation.country", "Isolation, sampling and environmental information.isolation.continent", "Safety information.risk assessment.biosafety level", "Sequence information.16S sequences.length", "Culture and growth conditions.culture medium.growth", "Morphology.colony morphology.incubation period", "Physiology and metabolism.metabolite production.metabolite", "Physiology and metabolism.metabolite production.production", "Safety information.risk assessment.pathogenicity animal", "Morphology.cell morphology.gram stain", "Morphology.cell morphology.cell shape", "Physiology and metabolism.spore formation.spore formation", "Sequence information.GC content.GC-content"]
                    # Write columns to file of the following structure: taxonomic ranks -> # of strains per species found on Bacdive -> column of interest flattened
                    file2 = open(os.path.join(output_dir, '%s_Flattened_Bacdive_data.tsv' % sample_name), "w")
                    file2.write(" " + "\t" + "Kingdom" + "\t" + "Phylum" + "\t" + "Class" + "\t" + "Order" + "\t" + "Family" + "\t" + "Genus" + "\t" + "Species" + "\t" + "Number of strains" + "\t" + "\t".join(str(interested_col) for interested_col in columns_of_interest) + "\n")

                    # Iterate throguh taxtable and if species unknown or not in Bacdive, fill everything with NA, else stored respective flattened values for the columns of interest
                    for ind in final_df.index:
                        kingdom = str(final_df['Kingdom'][ind])
                        phylum = str(final_df['Phylum'][ind])
                        class_rank = str(final_df['Class'][ind])
                        order = str(final_df['Order'][ind])
                        family = str(final_df['Family'][ind])
                        genus = str(final_df['Genus'][ind])
                        species = str(final_df['Species'][ind])

                        full_species = genus + " " + species

                        # If full species name is contained in resulting dataframe, then get strain count and flattened values
                        if (resulting_df["Name and taxonomic classification.species"] == full_species).any() == True:
                            strain_number = len(resulting_df.loc[resulting_df["Name and taxonomic classification.species"] == full_species].index)
                            list_results_interested_columns = []
                            # Get majority of non-na values and nan if information for all strains is nan
                            for interested_col in columns_of_interest:
                                first_cat_col = (resulting_df.loc[resulting_df["Name and taxonomic classification.species"] == full_species][interested_col]).dropna().tolist()
                                if len(first_cat_col) != 0:
                                    value = max(set(first_cat_col), key=first_cat_col.count)
                                    list_results_interested_columns.append(value)
                                else:  # if no information is there for any strain of a given spieces then add nan
                                    value = "nan"
                                    list_results_interested_columns.append(value)
                            # Write to file
                            file2.write(str(ind) + "\t" + kingdom + "\t" + phylum + "\t" + class_rank + "\t" + order + "\t" + family + "\t" + genus + "\t" + species + "\t" + str(strain_number) + "\t" + "\t".join(str(list_results_interested_columns[item]) for item in range(len(list_results_interested_columns))) + "\n")
                        # If not contained in bacdive or species is unknown, then fill up all following columns with NA's
                        else:
                            file2.write(str(ind) + "\t" + kingdom + "\t" + phylum + "\t" + class_rank + "\t" + order + "\t" + family + "\t" + genus + "\t" + species + "\t" + "nan" + "\t" + "\t".join("nan" for item in range(len(columns_of_interest))) + "\n")
                    file2.close()
        else:
            print(
                'If you have not registered for Bacdive web services yet, please do so using the following link before running this package: ' + 'https://sso.dsmz.de/auth/realms/DSMZ/protocol/openid-connect/auth?response_type=code&redirect_uri=https%3A%2F%2Fapi.bacdive.dsmz.de%2Flogin&client_id=api.bacdive&nonce=fc4f465de78388722385d9bd3f82de1f&state=cab5a9d249f9502bd01f7715cc5d99bd&scope=openid')
            print('Only try calling this function after gaining access.')
            exit(1)
    except AttributeError:
        print("Your login credentials were wrong. Please try again!")
        sys.exit(1)


if __name__=="__main__":
    bacdive_call()
