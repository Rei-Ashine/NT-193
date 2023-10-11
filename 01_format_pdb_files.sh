#!/usr/bin/bash
#$ -S /usr/bin/bash
# Author: rei-ashine
# DATE: Sep. 25th, 2023
# UPDATE: Oct. 11th, 2023
# bash 01_format_pdb_files.sh &>> logs/formatting.log

echo
echo "========== Executing $(basename "$0") =========="
cd "$(dirname "$0")" || exit
date

# shellcheck disable=SC1091
source config

# shellcheck source=/dev/null
source "$(conda info --base)"/etc/profile.d/conda.sh
conda activate nt-193

echo ----------
bash --version
echo
echo ----------
python --version
echo


START=$(date +%s)
echo ----------
echo "Formatting PDB files to compatible versions for PDBePISA ..."
for filename in "${PDB}"/*.pdb; do
	folder=$(basename "${filename%/*}")
	python scripts/format_pdb_file.py -i "${filename}" -o "${folder}"
done
wait
echo


END=$(date +%s)
echo --------------------
PT=$((END - START))
H=$((PT / 3600))
PT=$((PT % 3600))
M=$((PT / 60))
S=$((PT % 60))
echo "Execution time for $(basename "$0") : ${H}:${M}:${S}"
wait
echo ====================
echo
