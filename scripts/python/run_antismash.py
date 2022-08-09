#!/usr/bin/env python

import argparse, os, subprocess
from pathlib import Path
from shutil import copyfile

parser = argparse.ArgumentParser(
        description='''run antiSMASH on *.fna genome files''')

# add the parser arguments
parser.add_argument("input_dir", type=str, help="path/to/dir/with/genomes.fna/")
parser.add_argument("output_dir", type=str, help="path/to/output/")
parser.add_argument("thread_num", type=str, help="thread number")

args=parser.parse_args()

input_path = args.input_dir
output_path = args.output_dir
w = args.thread_num

# make the output directories if they do not exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

for file in os.listdir(input_path):
        if file.endswith(".fna"):
            in_prefix = file.split(".fna")[0]
            # makes a directory for each genome if it does not exist
            if not os.path.exists(output_path+in_prefix):
                os.makedirs(output_path+in_prefix)
            antismash_call = "antismash -c "+w+" --taxon bacteria --clusterblast --knownclusterblast --smcogs --outputfolder "+output_path+in_prefix+" "+input_path+file
            subprocess.call(antismash_call, shell=True)