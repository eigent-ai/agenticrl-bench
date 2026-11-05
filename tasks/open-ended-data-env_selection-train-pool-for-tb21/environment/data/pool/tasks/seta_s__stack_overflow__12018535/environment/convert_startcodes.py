#!/usr/bin/env python3
"""Convert 4-byte Annex B start codes to 3-byte start codes.

Replaces all occurrences of 00 00 00 01 with 00 00 01 in a raw
H.264 bitstream file.
"""

import sys


def convert(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()

    result = data.replace(b'\x00\x00\x00\x01', b'\x00\x00\x01')

    with open(output_path, 'wb') as f:
        f.write(result)

    print(f"Converted {input_path} -> {output_path}")
    print(f"  Input size: {len(data)} bytes")
    print(f"  Output size: {len(result)} bytes")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: convert_startcodes.py <input.264> <output.264>",
              file=sys.stderr)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
