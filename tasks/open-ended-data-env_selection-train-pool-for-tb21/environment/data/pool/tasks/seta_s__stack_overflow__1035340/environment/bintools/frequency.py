"""Byte frequency analysis module."""

from collections import Counter


def frequency(path):
    """Print a byte frequency histogram for the given file.

    Reads the file byte by byte and counts occurrences of each byte value.
    Output is sorted by byte value, showing hex value and count.

    Args:
        path: Path to the binary file to analyze.
    """
    counts = Counter()

    with open(path, "rb") as f:
        byte = f.read(1)
        while byte != "":
            counts[byte[0]] += 1
            byte = f.read(1)

    if not counts:
        print("Empty file.")
        return

    print(f"{'Byte':>6s}  {'Count':>6s}  {'Bar'}")
    print("-" * 40)

    for value in sorted(counts.keys()):
        count = counts[value]
        bar = "#" * min(count, 50)
        print(f"  0x{value:02x}  {count:6d}  {bar}")

    print("-" * 40)
    print(f"Total bytes: {sum(counts.values())}")
