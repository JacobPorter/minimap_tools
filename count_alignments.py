#!/usr/bin/env python
"""
Count the alignment types in minimap sam file
Jacob S. Porter jsporter@virginia.edu
"""
import argparse
import pickle
import sys

from SeqIterator import SeqReader


def compute_stats(sam_file_location, pickle_loc="./read_dictionary.pck"):
    read_dictionary = {}
    unmapped = 0
    nmis_num = 0
    nmis_denom = 0
    sam_file = SeqReader(sam_file_location, file_type="sam")
    mapped = 0
    for record in sam_file:
        id = record["QNAME"]
        flag = int(record["FLAG"])
        nmi = None
        if "NM:i" in record:
            nmi = int(record["NM:i"])
        if id not in read_dictionary:
            read_dictionary[id] = {"FLAG": flag, "NM:i": nmi}
            if nmi:
                nmis_num += nmi
                nmis_denom += 1
            if flag == 4:
                unmapped += 1
            else:
                mapped += 1
    if pickle_loc:
        pickle.dump(read_dictionary, open(pickle_loc, "wb"))
    return {
        "mapped": mapped,
        "unmapped": unmapped,
        "perc_map": mapped / (mapped + unmapped) * 100,
        "avg_nmi": nmis_num / nmis_denom,
        "total": mapped + unmapped,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sam_file", help="Location of SAM file.", type=str)
    parser.add_argument(
        "--read_dic_loc",
        help="Where to store the pickled read dictionary.",
        type=str,
        default=None,
    )
    map_args = parser.parse_args()
    print("Processing file: " + map_args.sam_file)
    print(
        "Percent mapped: {perc_map}%, Average edit distance: {avg_nmi}, Mapped: {mapped}, Unmapped: {unmapped}, Total reads: {total}".format_map(
            compute_stats(map_args.sam_file, map_args.read_dic_loc)
        ),
        file=sys.stdout,
    )


if __name__ == "__main__":
    main()
