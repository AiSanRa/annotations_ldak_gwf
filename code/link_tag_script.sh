#!/bin/bash
#SBATCH --partition normal
#SBATCH --account "name_of_the_account"
#SBATCH --mem 80gb
#SBATCH -- 10:00:00

code_path=$2
annot_path=$1

ln -s "$code_path"/ldak5.2.linux "$annot_path"/ldak5.2.linux
ln -s "$code_path"/tags.sh "$annot_path"/tags.sh
