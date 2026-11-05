#!/usr/bin/env python3
"""Data pipeline: reads input files and produces a summary report."""
import glob
import json
import os

INPUT_DIR = "/srv/pipeline/input/"
OUTPUT_DIR = "/srv/pipeline/output/processed/results/"


def find_input_files(directory):
    return glob.glob(os.path.join(directory, "*.csv"))


def compute_total_size(file_list):
    return sum(os.path.getsize(f) for f in file_list)


def main():
    files = find_input_files(INPUT_DIR)
    total_size = compute_total_size(files)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    summary = {
        "processed_files": len(files),
        "total_size_bytes": total_size,
    }

    output_path = os.path.join(OUTPUT_DIR, "summary.json")
    with open(output_path, "w") as fh:
        json.dump(summary, fh, indent=2)

    print(f"Processed {len(files)} files, {total_size} bytes total.")
    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    main()
