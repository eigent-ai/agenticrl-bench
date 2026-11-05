#!/usr/bin/env python3
"""Migration duplicate filename checker.

Scans a content directory for duplicate filenames that would cause
conflicts when migrating to a case-insensitive filesystem.

Usage: python3 dedup_check.py /path/to/directory
"""

import os
import sys


def check_duplicates(directory):
    """Check for duplicate filenames in the given directory."""
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)

    print(f"Scanning {directory} for duplicate filenames...")

    entries = os.listdir(directory)
    files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]

    print(f"Found {len(files)} files to check.")

    seen = set()
    duplicates = []
    for f in files:
        if f in seen:
            duplicates.append(f)
        seen.add(f)

    if duplicates:
        print(f"WARNING: Found {len(duplicates)} duplicate filenames:")
        for d in duplicates:
            print(f"  - {d}")
        return 1
    else:
        print("All clear! No duplicate filenames found.")
        return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(check_duplicates(target))
