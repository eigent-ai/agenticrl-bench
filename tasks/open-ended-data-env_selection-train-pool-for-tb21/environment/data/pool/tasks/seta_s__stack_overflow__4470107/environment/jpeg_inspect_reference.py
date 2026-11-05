#!/usr/bin/env python3
import sys
import json
import numpy as np
import scipy.fft
from PIL import Image


def analyze_jpeg(path):
    img = np.array(Image.open(path).convert('L'))
    h, w = img.shape
    blocks = []
    for r in range(0, h - h % 8, 8):
        for c in range(0, w - w % 8, 8):
            block = img[r:r+8, c:c+8].astype(float) - 128.0
            dct_block = scipy.fft.dctn(block, norm='ortho')
            dc_coeff = float(dct_block[0, 0])
            ac_energy = float(np.sum(dct_block**2) - dct_block[0, 0]**2)
            blocks.append({"row": r // 8, "col": c // 8, "dc_coeff": dc_coeff, "ac_energy": ac_energy})
    return {
        "filename": path,
        "image_size": {"height": h, "width": w},
        "block_count": len(blocks),
        "blocks": blocks
    }


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    result = analyze_jpeg(input_path)
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Analyzed {result['block_count']} blocks from {input_path}")
