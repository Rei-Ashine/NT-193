#!/usr/bin/bash
#$ -S /usr/bin/bash
# Author: rei-ashine
# DATE: Sep. 26th, 2023
# bash batch_converter.sh [foldername]


for filename in "$1"/*.pdb; do
    # Handle the case of no *.pdb files
    [[ -e "$filename" ]] || break
    git mv "$filename" "${filename/\`/_}"
done
