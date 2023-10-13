#!/usr/bin/bash
#$ -S /usr/bin/bash
# Author: rei-ashine
# DATE: Oct. 12th, 2023
# bash batch_renamer.sh [foldername]


for filename in "$1"/*.pdb; do
    # Handle the case of no *.pdb files
    [[ -e "$filename" ]] || break
	# Rename
	string_to_replace="7e5o_GlobalMinimized_formatted_"
	if [[ "$filename" == *"$string_to_replace"* ]]; then
		echo "[INFO] The file has already been renamed."
	else
		echo "Renaming ..."
		echo "Before : ${filename}"
		echo "After  : ${filename/7e5o_GlobalMinimized_/7e5o_GlobalMinimized_formatted_}"
		git mv "$filename" "${filename/7e5o_GlobalMinimized_/7e5o_GlobalMinimized_formatted_}"
		echo "done."
		echo
	fi
done
