#!/usr/bin/env python

import argparse, os, subprocess

parser = argparse.ArgumentParser(
        description='''processes amplicon reads with fastp''')

# add the parser arguments
parser.add_argument("input", type=str, help="path/to/input/dir/")
parser.add_argument("output", type=str, help="path/to/output/dir/")
parser.add_argument("threads", type=str, help="number of threads")

args=parser.parse_args()

input_path = args.input
output_path = args.output
threads_num = args.threads

# make the output directory if it doesn't exist

if not os.path.exists(output_path+"processed_reads/"):
    os.makedirs(output_path+"processed_reads/")

if not os.path.exists(output_path+"processed_reads_reports/"):
    os.makedirs(output_path+"processed_reads_reports/")

for file in os.listdir(input_path):
    if file.endswith("_R1.fastq.gz"):
        file_prefix = file.split("_R1.fastq.gz")[0]
        fastp_call = "fastp -i "+input_path+file_prefix+"_R1.fastq.gz"+" -I "+input_path+file_prefix+"_R2.fastq.gz"+" -o "+output_path+"processed_reads/"+file_prefix+"_out_R1.fastq.gz"+" -O "+output_path+"processed_reads/"+file_prefix+"_out_R2.fastq.gz"+" -h "+output_path+"processed_reads_reports/"+file_prefix+".html -j "+output_path+"processed_reads_reports/"+file_prefix+".json"+" -w "+threads_num
        subprocess.call(fastp_call, shell=True)