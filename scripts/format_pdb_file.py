# Author: rei-ashine
# DATE: Sep. 20th, 2023
# UPDATE: Sep. 21st, 2023

"""
Format a PDB file from MolDesk to a PDB file that PDBePISA can interpret.
"""

import os
import os.path
import re
import pprint
import argparse


def delete_lines(line, ng_words):
    """
    Remove lines containing a specific string from a file.
    """
    flag = False
    for i in ng_words:
        if i in line:
            flag = True
            break
    return flag


def replace_words(line, logs):
    """
    Replace a specific string in a given line.
    """
    # Replace "CYSS" with "CYS "
    cyss = re.findall("CYSS", line)
    assert len(cyss) <= 1, \
        "[Warning] The line contains an unknown pattern, \
        and the string cannot be replaced."
    if len(cyss) == 1:
        logs["CYSS"] += 1

    wo_cyss = re.sub("CYSS", "CYS ", line)

    # Replace "+/-[A..Z]" with " [A..Z]"
    pattern1 = re.compile(r"[\+\-][A-Z]{1}")
    target = re.findall(pattern1, wo_cyss)
    assert len(target) <= 1, \
        "[Warning] The line contains an unknown pattern, \
        and the string cannot be replaced."
    if len(target) == 1:
        if target[0] in logs:
            logs[target[0]] += 1
        else:
            logs[target[0]] = 1

    pattern2 = re.compile(r"([\+\-])([A-Z]{1})")
    replaced = pattern2.sub(r" \2", wo_cyss)

    return replaced, logs


def formatter(input_moldesk, output_file, ng_words):
    """
    Format a PDB file from MolDesk to a PDB file that PDBePISA can interpret.
    """
    count_lines = 0
    count_deletion = 0
    logs = {"CYSS": 0}
    with open(output_file, encoding="utf-8", mode="w") as file:
        for line in open(input_moldesk, encoding="utf-8", mode="r"):

            count_lines += 1
            if delete_lines(line, ng_words):
                count_deletion += 1
            else:
                line, logs = replace_words(line, logs)
                file.write(line)

    print(f"[INFO] The input PDB file has {count_lines} lines.")
    print(f'[INFO] {count_deletion} lines that contain the "SSBOND" line are deleted.')

    print("[INFO] Replaced strings and the number of occurrences")
    pprint.pprint(logs)
    total = sum(logs.values())
    print(f"[INFO] Total number of replaced strings : {total}")

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
