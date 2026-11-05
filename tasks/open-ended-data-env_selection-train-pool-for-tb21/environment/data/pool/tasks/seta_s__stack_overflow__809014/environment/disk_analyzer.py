#!/usr/bin/env python3
"""Disk usage analyzer — reports recursive sizes of a directory tree."""
import os
import json
import sys


def get_dir_size(path):
    """Return total bytes of all files under path."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path, followlinks=True):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    return total


def analyze_directory(root_path):
    results = {}
    file_count = 0

    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path) and not os.path.islink(item_path):
            if not item.startswith('.'):
                results[item] = get_dir_size(item_path)
        elif os.path.isfile(item_path):
            file_count += 1

    total = get_dir_size(root_path)

    subdirs = sorted(
        [{"name": k, "bytes": v} for k, v in results.items()],
        key=lambda x: x["bytes"]
    )

    return {
        "total_bytes": total,
        "subdirectories": subdirs,
        "file_count": file_count,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: disk_analyzer.py <directory> <output_json>")
        sys.exit(1)
    report = analyze_directory(sys.argv[1])
    with open(sys.argv[2], "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"Report written to {sys.argv[2]}")
