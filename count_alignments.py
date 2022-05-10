#!/usr/bin/env python
"""
Count the alignment types in minimap sam file
Jacob S. Porter jsporter@virginia.edu
"""
import argparse
import sys

from SeqIterator import SeqReader


def compute_stats(sam_file_location):
    read_dictionary = {}
    unmapped = 0
    sam_file = SeqReader(sam_file_location, file_type="sam")
    for record in sam_file:
        id = record["QNAME"]
        flag = record["FLAG"]
        nmi = None
        if "NM:i" in record:
            nmi = record["NM:i"]
        if id not in read_dictionary:
            read_dictionary[id] = {"FLAG": flag, "NM:i": nmi}
            if flag == 4:
                unmapped += 1
            else:
                mapped += 1
    return (mapped, unmapped)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sam_file", help="Location of SAM file.", type=str)
    map_args = parser.parse_args()
    print("Processing file: " + map_args.sam_file)
    print(
        "Mapped: {}, Unmapped: {}" % compute_stats(map_args.sam_file), file=sys.stdout
    )


if __name__ == "__main__":
    main()
