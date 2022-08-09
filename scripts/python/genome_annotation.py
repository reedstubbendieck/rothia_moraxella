#!/usr/bin/env python

import argparse, csv, os, subprocess
import pandas as pd

parser = argparse.ArgumentParser(
        description='''runs prokka on genome sequences to predict protein coding genes''')

# add the parser arguments
parser.add_argument("input_dir", type=str, help="path/to/input/")
parser.add_argument("output_dir", type=str, help="path/to/output/")
parser.add_argument("genome_table_path", type=str, help="path/to/genome_table.csv/")
parser.add_argument("thread_num", type=str, help="number of threads")

args=parser.parse_args()

input_path = args.input_dir
output_path = args.output_dir
table_path = args.genome_table_path
w = args.thread_num

# load in the genome_table
genome_table = pd.read_csv(table_path, comment='#', delimiter=",", header=0)

# initialize dictionarys for genus and species

genus_dict = pd.Series(genome_table.genus.values,index=genome_table.strain).to_dict()
species_dict = pd.Series(genome_table.species.values,index=genome_table.strain).to_dict()

# run prokka on each genome in the input_path

for file in os.listdir(input_path):
       if file.endswith(".fna"):
            file_prefix = file.split(".fna")[0]
            prokka_call = "prokka --outdir "+output_path+file_prefix+" --prefix "+file_prefix+" --genus "+genus_dict[file_prefix]+" --species "+species_dict[file_prefix]+" --strain "+file_prefix+" --cpus "+w+" "+input_path+file
            subprocess.call(prokka_call, shell=True)