#!/usr/bin/bash
#$ -S /usr/bin/bash
# Author: rei-ashine
# DATE: Sep. 25th, 2023
# bash 01_format_pdb_files.sh &>> logs/formatting.log

echo
echo "========== Executing $(basename $0) =========="
cd $(dirname $0)
date

source ./config

echo ----------
bash --version
echo
echo ----------
python --version
echo


START=$(date +%s)
echo ----------
echo "Formatting PDB files to compatible versions for PDBePISA ..."
for filename in ${PDB}/*.pdb; do
		folder=$(basename ${filename%/*})
		python scripts/format_pdb_file.py -i ${filename} -o ${folder}
done
wait
echo


END=$(date +%s)
echo --------------------
PT=$(expr ${END} - ${START})
H=$(expr ${PT} / 3600)
PT=$(expr ${PT} % 3600)
M=$(expr ${PT} / 60)
S=$(expr ${PT} % 60)
echo "Execution time for $(basename $0) : ${H}:${M}:${S}"
wait
echo ====================
echo
