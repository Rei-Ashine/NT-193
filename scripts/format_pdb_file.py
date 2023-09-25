# Author: rei-ashine
# DATE: Sep. 20th, 2023
# UPDATE: Sep. 25th, 2023

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


def count_patterns(pattern, line, logs):
    """
    Count the number of occurrences of a particular string.
    """
    target = re.findall(pattern, line)
    assert len(target) <= 1, \
        "[Warning] The line contains an unknown pattern, and the string cannot be replaced."

    if len(target) == 1:
        token = "".join(target[0])
        if token in logs:
            logs[token] += 1
        else:
            logs[token] = 1
    return logs


def replace_words(line, logs):
    """
    Replace a specific string in a given line.
    """
    # Replace "CYSS[A..Z]" with "CYS [A..Z]"
    pattern1 = re.compile(r"(CYSS)([A-Z]{1})")
    logs = count_patterns(pattern1, line, logs)
    wo_cyss = pattern1.sub(r"CYS \2", line)

    # Replace "+/-[A..Z]" with " [A..Z]"
    pattern2 = re.compile(r"([\+\-])([A-Z]{1})")
    logs = count_patterns(pattern2, line, logs)
    replaced = pattern2.sub(r" \2", wo_cyss)

    return replaced, logs


def formatter(input_moldesk, output_file, ng_words):
    """
    Format a PDB file from MolDesk to a PDB file that PDBePISA can interpret.
    """
    count_lines = 0
    count_deletion = 0
    logs = dict()
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
    print(f"[INFO] {len(logs)} different string patterns in the file needed to be replaced.")

    rest = count_lines - count_deletion
    print(f"[INFO] Output PDB file name : {os.path.basename(output_file)}")
    print(f"[INFO] The output PDB file has {rest} lines.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True,
                        help="Set the input PDB file path")
    parser.add_argument("-o", "--output", required=True,
                        help="Set the output directory name")
    args = parser.parse_args()
    print("----- START -----")

    # Load an input PDB file
    path = args.input
    basename = os.path.basename(path)
    print(f"[INFO] Input PDB file name : {basename}")

    # Confirm the existence of the output file/folder
    temp = f"data/Formatted/{args.output}"
    if not os.path.isdir(temp):
        os.makedirs(temp)
    filename = os.path.splitext(os.path.basename(path))[0]
    path_output = f"{temp}/{filename}_formatted.pdb"

    assert not os.path.isfile(path_output), \
        "[Warning] The input PDB file is already formatted."

    # Format a PDB file
    NG_words = ["SSBOND"]
    formatter(path, path_output, NG_words)

    print("----- END -----")
