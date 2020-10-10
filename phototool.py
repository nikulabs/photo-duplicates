#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time
from datetime import timedelta
from itertools import chain
from pathlib import Path
from typing import Dict, List

import imagehash
from PIL import Image
from imagehash import ImageHash


def parse_args():
    parser = argparse.ArgumentParser(
        description='Finds duplicates in the given directory.'
    )
    parser.add_argument("-d", "--directory", help="The directory in which to search")
    parser.add_argument("-r", "--recursive", help="Also search subdirectories",
                                             action="store_true")
    return parser.parse_args()


def find_photos(working_dir: Path, glob: str) -> List[Path]:
    def is_image(filename: Path):
        return filename.suffix.lower() in [".png", ".jpg", ".jpeg", "bmp", ".gif", ".svg"]
    return [path for path in working_dir.glob(glob) if is_image(path)]

def compute_hashes(photos: List[Path]) -> Dict[Path, ImageHash]:
    return {photo:imagehash.average_hash(Image.open(photo)) for photo in photos}

def compute_hamming_distance(photos: Dict[Path, ImageHash], verbose=False) -> List[List[int]]:
    matrix = [[0] * len(photos) for i in range(len(photos))]
    for i, lhs in enumerate(photos.values()):
        for j, rhs in enumerate(photos.values()):
            matrix[i][j] = abs(rhs-lhs)
    if verbose:
        for row in matrix:
            print(row)
    return matrix

def group_photos_by_distance(photos: List[Path], distance_matrix: List[List[int]], verbose=False) -> List[List[Path]]:
    grouped_indices = []
    matched = []
    for i, row in enumerate(distance_matrix):
        if i in matched:
            continue
        matches_in_row = [i for i, distance in enumerate(row) if distance <= 5]
        grouped_indices.append(matches_in_row)
        matched.extend(matches_in_row)
    
    if verbose:
        for index in grouped_indices:
            print(index)

    grouped_photos = []
    for indices in grouped_indices:
        duplicate_photos = [photos[i] for i in indices]
        grouped_photos.append(duplicate_photos)

    if verbose:
        for photo in grouped_photos:
            print(str(photo))


def main():
    args = parse_args()

    working_dir = Path(args.directory) if args.directory else Path()
    glob = "**/*" if args.recursive else "*"

    start = time.time()
    photo_paths = find_photos(working_dir, glob)
    print(f"Time to find photos: {timedelta(seconds=time.time() - start)}")

    start = time.time()
    photo_hashes = compute_hashes(photo_paths)
    print(f"Time to compute hashes: {timedelta(seconds=time.time() - start)}")

    start = time.time()
    hamming_distance_matrix = compute_hamming_distance(photo_hashes)
    print(f"Time to create hamming distance matrix: {timedelta(seconds=time.time() - start)}")

    start = time.time()
    grouped_photos = group_photos_by_distance(photo_paths, hamming_distance_matrix)
    print(f"Time to group photos by distance: {timedelta(seconds=time.time() - start)}")
    return 0


if __name__ == "__main__":
    main()
