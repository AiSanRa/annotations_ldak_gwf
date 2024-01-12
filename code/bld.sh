#!/bin/bash
#SBATCH --partition normal
#SBATCH --account "name_of_the_account"
#SBATCH --mem 80gb
#SBATCH -- 10:00:00

annotations=$1
blds=$2

# Loop through each subfolder in the annotations folder
find "$annotations" -mindepth 1 -type d | while read -r subfolder; do
    for file in "$blds"/bld* ; do
        if [[ ! $(basename "$file") =~ ^bldnames ]]; then
            ln -s "$file" "$subfolder/$(basename "$file")"
        fi
    done
done