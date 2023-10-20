#!/usr/bin/bash
#$ -S /usr/bin/bash
# Author: rei-ashine
# DATE: Oct. 20th, 2023
# bash 02_visualize_pisa_scores.sh &>> logs/visualizing.log

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
echo "Creating scatter plots from PISA score CSV files ..."
for filename in "${PISA}"/*.csv; do
	python scripts/visualize_pisa_scores.py -i "${filename}"
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
