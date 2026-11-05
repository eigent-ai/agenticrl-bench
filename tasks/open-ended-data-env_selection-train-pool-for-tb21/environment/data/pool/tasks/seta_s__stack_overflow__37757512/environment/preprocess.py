#!/usr/bin/env python3
"""Normalize whitespace in OCR text files.

Usage: python3 preprocess.py file1.txt file2.txt ...

Collapses multiple spaces into one and strips leading/trailing
whitespace from each line. Writes changes back in-place.
"""

import sys
import re


def normalize_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
        lines = f.readlines()

    normalized = []
    for line in lines:
        line = line.rstrip('\n').rstrip('\r')
        line = re.sub(r'[ \t]+', ' ', line)
        line = line.strip()
        normalized.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(normalized) + '\n')


def main():
    if len(sys.argv) < 2:
        print("Usage: preprocess.py <file1> [file2] ...", file=sys.stderr)
        sys.exit(1)

    for fpath in sys.argv[1:]:
        normalize_file(fpath)


if __name__ == '__main__':
    main()
