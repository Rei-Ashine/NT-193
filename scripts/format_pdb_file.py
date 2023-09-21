# Author: rei-ashine
# DATE: Sep. 20th, 2023
# UPDATE: Sep. 21st, 2023

"""
Format a PDB file from MolDesk to a PDB file that PDBePISA can interpret.
"""

import os
import os.path
import re
import argparse


def delete_lines(line, ng_words):
    """
    Remove lines containing a specific string from a file.
    """
    status = False
    for i in ng_words:
        if i in line:
            status = True
            break
    return status


def replace_words(line):
    """
    Replace a specific string in a given line.
    """
    wo_cyss = re.sub("CYSS", "CYS ", line)
    return wo_cyss


def formatter(input_moldesk, output_file, ng_words):
    """
    Format a PDB file from MolDesk to a PDB file that PDBePISA can interpret.
    """
    count_lines = 0
    count_deletion = 0
    with open(output_file, encoding="utf-8", mode="w") as file:
        for line in open(input_moldesk, encoding="utf-8", mode="r"):

            count_lines += 1
            if delete_lines(line, ng_words):
                count_deletion += 1
            else:
                line = replace_words(line)
                file.write(line)

    print(f"[INFO] The input PDB file has {count_lines} lines.")
    print(f"[INFO] {count_deletion} lines are deleted.")

    rest = count_lines - count_deletion
    print(f"[INFO] Output PDB file name : {os.path.basename(output_file)}")
    print(f"[INFO] The output PDB file has {rest} lines.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True,
                        help="Set the input PDB file path")
    parser.add_argument("-o", "--output", default="data/Formatted",
                        help="Set the output directory name")
    args = parser.parse_args()
    print("----- START -----")

    # Load an input PDB file
    path = args.input
    basename = os.path.basename(path)
    print(f"[INFO] Input PDB file name : {basename}")

    # Confirm the existence of the output file/folder
    if not os.path.isdir(args.output):
        os.makedirs(args.output)
    filename = os.path.splitext(os.path.basename(path))[0]
    path_output = f"{args.output}/{filename}_formatted.pdb"

    assert not os.path.isfile(path_output), \
        "[Warning] The input PDB file is already formatted."

    # Format a PDB file
    NG_words = ["SSBOND"]
    formatter(path, path_output, NG_words)

    print("----- END -----")
