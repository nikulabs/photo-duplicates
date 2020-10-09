#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from collections import defaultdict
from itertools import chain
from pathlib import Path
from PIL import Image
import imagehash

def parse_args():
    parser = argparse.ArgumentParser(
        description='Finds duplicates in the given directory.'
    )
    parser.add_argument("-d", "--directory", help="The directory in which to search")
    parser.add_argument("-r", "--recursive", help="Also search subdirectories",
                                             action="store_true")
    return parser.parse_args()

def compute_hashes(working_dir, glob):

    def is_image(filename: Path):
        return filename.suffix.lower() in [".png", ".jpg", ".jpeg", "bmp", ".gif", ".svg"]

    hashes = dict()
    for path in working_dir.glob(glob):
        if is_image(path):
            im = Image.open(path)
            hash = imagehash.average_hash(im)
            hashes[path] = hash
    return hashes

def compute_hamming_distance(photos: dict):
    matrix = [[0] * len(photos) for i in range(len(photos))]
    for i, lhs in enumerate(photos):
        for j, rhs in enumerate(photos):
            matrix[i][j] = abs(rhs-lhs)
    return matrix

def find_duplicates(hashes, threshold=5):
    """
    Group elements in a dictionary by the key value.
    As long as sorted consecutive keys are less different than the threshold, group the elements together.
    Imposes ordering on the dictionary.
    """
    sorted_hashes = sorted(hashes.keys())
    groups = [[sorted_hashes[0]]] # Seed first group with first hash
    for lhs, rhs in zip(sorted_hashes[:-1], sorted_hashes[1:]):
        if abs(lhs-rhs) <= threshold:
            groups[len(groups)-1].append(rhs)
        else:
            groups.append([rhs])
    duplicates = {}
    for group in groups:
        duplicates[tuple(group)] = list(chain.from_iterable([hashes[hash] for hash in group]))
    return duplicates

def main():
    args = parse_args()

    working_dir = Path(args.directory) if args.directory else Path()
    glob = "**/*" if args.recursive else "*"
    photo_hashes = compute_hashes(working_dir, glob)
    hamming_distance = compute_hamming_distance(photo_hashes)
    for i, photo in enumerate(hamming_distance):
        near_duplicates = [j for j, distance in enumerate(photo) if distance <= 5]
        if len(near_duplicates) == 1:
            unique.append(photo)

    for key, value in near_duplicates.items():
        print(f"{False}")


    keys = list(photo_hashes.keys())
    differences = [(lhs, rhs, abs(lhs-rhs)) for lhs, rhs in zip(keys[:-1], keys[1:])]
    for lhs, rhs, difference in differences:
        print(f"{lhs} - {rhs} = {difference}")

    for key, value in photo_hashes.items():
        print(f"{key}:\n\t", end='')
        print("\n\t".join([str(path) for path in value]))

    return 0

if __name__ == "__main__":
    main()
