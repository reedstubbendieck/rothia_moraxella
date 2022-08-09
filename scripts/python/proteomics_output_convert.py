#!/usr/bin/python3

import argparse, os
import pandas as pd

parser = argparse.ArgumentParser(
        description='''processes the .xlsx output from proteomics experiments into a tidy format''')

# add the parser arguments
parser.add_argument("input_dir", type=str, help="path/to/dir/with/protemoics/output/")
parser.add_argument("output", type=str, help="path/to/output.tsv")

args=parser.parse_args()

input_path = args.input_dir
output_path = args.output

dataframe_list = []

for file in os.listdir(input_path):
        if file.endswith(".xlsx"):
            in_prefix = file.split(".xlsx")[0]
            proteomics_output = pd.read_excel(input_path+file, engine='openpyxl', skiprows=1, usecols=[1,2,3,4])
            # rename the columns to be more friendly to later processing
            proteomics_output.columns = ["protein", "accession", "molecular_weight", "spectrum_count"]
            # remove the kDa from the molecular weight column
            proteomics_output["molecular_weight"] = proteomics_output["molecular_weight"].str.replace(r'kDa', '')
            # add a new column to the data frame to indicate the strain
            proteomics_output["strain"] = in_prefix
            # reorder the columns
            proteomics_output = proteomics_output.reindex(["strain", "accession", "protein", "molecular_weight", "spectrum_count"], axis=1)
            dataframe_list.append(proteomics_output)

# concatenate the data frames together
combined_proteomics = pd.concat(dataframe_list)

# save the output data frame
combined_proteomics.to_csv(output_path, sep = "\t", header=True, index = False, index_label=False)