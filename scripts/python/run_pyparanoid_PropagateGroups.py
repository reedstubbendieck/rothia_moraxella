#!/usr/bin/env python

import argparse, os, subprocess
import pandas as pd
from pathlib import Path
from shutil import copyfile

parser = argparse.ArgumentParser(
        description='''processes prokka .faa output and runs pyparanoid to generate pangenome''')

# add the parser arguments
parser.add_argument("input_dir", type=str, help="path/to/dir/with/prokka/outputs/")
parser.add_argument("output_dir", type=str, help="path/to/output/")
parser.add_argument("strain_list_path", type=str, help="path/to/strainlist.txt")
parser.add_argument("database_name", type=str, help="database name")
parser.add_argument("thread_num", type=str, help="number of threads")

args=parser.parse_args()

input_path = args.input_dir
output_path = args.output_dir
strain_path = args.strain_list_path
DB_name = args.database_name
w = args.thread_num

# make the output directory if it does not exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

## also make the pep output directory if it does not exist
if not os.path.exists(output_path+"/pep/"):
    os.makedirs(output_path+"/pep/")

# copy and rename the prokka protein annotation files
for entry in Path(input_path).iterdir():
    # check if entry in path is a directory
    if entry.is_dir():
        # extract the .faa file for each entry in the directory, move, and rename for pyparanoid
        basename = entry.stem
        entry_path = str(entry)
        copyfile(entry_path+"/"+basename+".faa", output_path+"/pep/"+basename+".pep.fa")

# call pyparanoid
pyparanoid_call = "PropagateGroups.py --cpus "+w+" "+output_path+" "+strain_path+" "+output_path+DB_name
subprocess.call(pyparanoid_call, shell=True)