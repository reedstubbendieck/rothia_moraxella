# <i>Rothia</i> from the human nose inhibit <i>Moraxella catarrhalis</i> colonization with a secreted peptidoglycan endopeptidase

Reed M. Stubbendieck<sup>1,2</sup>, Eishika Dissanayake<sup>3</sup>, Peter M. Burnham<sup>1</sup>, Susan E. Zelasko<sup>1,4</sup>, Mia I. Temkin<sup>1</sup>, Sydney S. Wisdorf<sup>3</sup>, Rose F. Vrtis<sup>3</sup>, James E. Gern<sup>3,5</sup>, Cameron R. Currie<sup>1,6,7,8</sup>

<sup>1</sup>Department of Bacteriology, University of Wisconsin-Madison, Madison, WI 53706
<sup>2</sup>Department of Microbiology and Molecular Genetics, Oklahoma State University, Stillwater, OK 74078
<sup>3</sup>Department of Pediatrics, University of Wisconsin School of Medicine and Public Health, Madison, WI 53792
<sup>4</sup>Microbiology Doctoral Training Program, University of Wisconsin-Madison, Madison, WI 53706
<sup>5</sup>Department of Medicine, University of Wisconsin School of Medicine and Public Health, Madison, WI 53792
<sup>6</sup>Department of Energy Great Lakes Bioenergy Research Center, University of Wisconsin-Madison, Madison, WI 53706
<sup>7</sup>Laboratory of Genetics, University of Wisconsin-Madison, Madison, WI 53706
<sup>8</sup>David Braley Centre for Antibiotic Discovery, Department of Biochemistry and Biomedical Sciences, McMaster University, Hamilton, Ontario, Canada

## Introduction

This repository contains the code necessary to replicate the results and figures of our study on interactions between the pathobiont <i>Moraxella catarrhalis</i> and <i>Rothia</i>.

## Datasets

The code in the Rmd document and the following code snippets expect the raw and derived datasets to be in the ./rawData/ and ./derivedData/ directories, respectively.

### Raw datasets

The raw amplicon sequencing reads can be found in the Short Read Archive under BioProject accession [PRJNA866994](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA866994). The genome sequences of the *Rothia* generated for this study can be found under BioProject accession [PRJNA867425](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA867425). All other raw datasets can be found from FigShare: [here](https://doi.org/10.6084/m9.figshare.20444466).

### Derived datasets

All derived datasets can be found from FigShare: [here](https://doi.org/10.6084/m9.figshare.20444466).

## Prerequisites

### Software

* [antiSMASH](https://docs.antismash.secondarymetabolites.org/install/)
* [anvi'o](https://anvio.org/)
* [BiG-SCAPE](https://git.wageningenur.nl/medema-group/BiG-SCAPE)
* [Core Species Tree](https://github.com/chevrm/core_species_tree)
* [Mothur](https://mothur.org/)
* [Prokka](https://github.com/tseemann/prokka)
* [PyParanoid](https://github.com/ryanmelnyk/PyParanoid)

### R Packages
* [Biostrings](https://bioconductor.org/packages/release/bioc/html/Biostrings.html)
* [circlize](https://jokergoo.github.io/circlize_book/book/)
* [cowplot](https://cran.r-project.org/web/packages/cowplot/index.html)
* [ggmsa](http://yulab-smu.top/ggmsa/)
* [ggnewscale](https://cran.r-project.org/web/packages/ggnewscale/index.html)
* [ggpubr](https://cran.r-project.org/web/packages/ggpubr/index.html)
* [ggtree](https://bioconductor.org/packages/release/bioc/html/ggtree.html)
* [phyloseq](https://www.bioconductor.org/packages/release/bioc/html/phyloseq.html)
* [RColorBrewer](https://cran.r-project.org/web/packages/RColorBrewer/index.html)
* [readr](https://cran.r-project.org/web/packages/readr/index.html)
* [reshape2](https://cran.r-project.org/web/packages/reshape2/index.html)
* [rstatix](https://cran.r-project.org/web/packages/rstatix/index.html)
* [seqmagick](https://cran.rstudio.com/web/packages/seqmagick/index.html)
* [tidyverse](https://www.tidyverse.org/)
* [vegan](https://cran.r-project.org/web/packages/vegan/index.html)

## Code

For all code, the thread_num needs to be changed before it can be run. All paths below assume that code is being run from the base project directory.

### Processing reads with fastp

    python3 ./scripts/python/run_fastp.py ./rawData/amplicon_reads/ ./derivedData/amplicon_reads/processed_reads/ thread_num

### Mothur

    conda activate mothur
    mothur ./scripts/mothur/mothur_batch_file.txt
    conda deactivate

### Genome Annotation

    conda activate prokka
    python3 ./scripts/python/genome_annotation.py ./rawData/genomes/combined_genomes/ ./derivedData/annotations/combined_genomes/ ./rawData/genomes/rothia_genome_table.csv thread_num
    conda deactivate
    
## PyParanoid

    conda activate pyparanoid
    python3 ./scripts/python/run_pyparanoid_BuildGroups.py ./derivedData/annotations/combined_genomes/ ./derivedData/pyparanoid_out_combined/ ./rawData/genomes/combined_strainlist.txt RothiaDB thread_num
    python3 scripts/python/parse_homolog_faa.py ./derivedData/pyparanoid_out_combined/RothiaDB/homolog.faa ./derivedData/pyparanoid_out_combined/RothiaDB/rothia_homolog_groups.tsv
    conda deactivate
    
### Core Species Tree

    mkdir ./derivedData/phylogenetic_trees/rothia_tree/
    cd ./derivedData/phylogenetic_trees/rothia_tree/
    perl path/to/core_species_tree/core_species_tree.pl path/to/rawData/rothia_genomes/*.fna

Used FigTree to convert the ASTRAL-II core-genome phylogeny (./derivedData/rothia_tree/astral.species.tre) using propotional branch lengths based on the root (./derivedData/rothia_tree/astral.species_proportional.tre).

### anvi'o

    conda activate anvio-7
    python3 ./scripts/python/run_anvio.py ./rawData/genomes/combined_genomes/ ./derivedData/anvio_out/ Rothia thread_num
    anvi-import-misc-data -p ./derivedData/anvio_out/anvio_pangenome/Rothia-PAN.db -t layers ./rawData/genomes/rothia_genome_table.tsv
    anvi-compute-genome-similarity --external-genomes ./derivedData/anvio_out/external_genomes --program pyANI --output-dir ./derivedData/anvio_out/ANI/ --num-threads thread_num --pan-db derivedData/anvio_out/anvio_pangenome/Rothia-PAN.db
    anvi-display-pan -g ./derivedData/anvio_out/Rothia-GENOMES.db -p ./derivedData/anvio_out/anvio_pangenome/Rothia-PAN.db --server-only -P 8080
    anvi-script-add-default-collection -p ./derivedData/anvio_out/anvio_pangenome/Rothia-PAN.db
    anvi-summarize -g ./derivedData/anvio_out/Rothia-GENOMES.db -p ./derivedData/anvio_out/anvio_pangenome/Rothia-PAN.db -C DEFAULT
    conda deactivate

### antiSMASH

    conda activate antismash
    python3 ./scripts/python/run_antismash.py ./rawData/genomes/combined_genomes/ ./derivedData/rothia_antismash_output/ thread_num
    conda deactivate

### BiG-SCAPE

    conda activate bigscape
     python3 /home/stubbendieck/BiG-SCAPE/bigscape.py --pfam_dir /home/stubbendieck/databases/ -c thread_num --mibig --include_singletons --mix --hybrids-off --verbose -i ./derivedData/rothia_antismash_output/gbks/ -o ./derivedData/rothia_bigscape/
     conda deactivate

### Proteomics Output

    python3 ./scripts/python/proteomics_output_convert.py ./rawData/proteomics/ ./derivedData/rothia_proteomics_output.tsv

ymls

    antismash
    anvio-7
    bigscape
    mothur
    prokka
    pyparanoid
