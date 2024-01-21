#!/bin/bash
#SBATCH --partition normal
#SBATCH --account "name_of_the_account"
#SBATCH --mem 50gb
#SBATCH -- 10:00:00

name=$1
sums=$2
tag_name=$3

./ldak5.2.linux --sum-hers "$name" \ 
                --summary <(zcat "$sums") \
                --tagfile "$tag_name".tagging \
                --check-sums NO \
                --max-threads 8

touch done_heritability