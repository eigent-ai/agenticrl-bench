#!/usr/bin/env python3
"""Convert an sRGB PNG image to NV12 raw binary (BT.709)."""
import sys
import os
from rgb_to_nv12 import rgb_to_nv12_bt709


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.png> <output.raw>")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found")
        sys.exit(1)

    nv12 = rgb_to_nv12_bt709(input_path, output_path)
    h, w = nv12.shape
    print(f"Converted: {input_path} -> {output_path}")
    print(f"Shape: {nv12.shape}, dtype: {nv12.dtype}")
    print(f"Y[0,0]={nv12[0,0]}  UV[{h*2//3},0]={nv12[h*2//3, 0]}  UV[{h*2//3},1]={nv12[h*2//3, 1]}")


if __name__ == '__main__':
    main()
