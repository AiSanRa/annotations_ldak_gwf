#!/bin/bash
#SBATCH --partition normal
#SBATCH --account "name_of_the_account"
#SBATCH --mem 50gb
#SBATCH -- 10:00:00

tag_name=$1
plink_path=$2

./ldak5.2.linux --calc-tagging "$tag_name" \
                --bfile "$plink_path" \
                --ignore-weights YES \
                --power -0.25 \
                --window-kb 1000 \
                --annotation-number 66 \
                --annotation-prefix bld

touch done_tagging