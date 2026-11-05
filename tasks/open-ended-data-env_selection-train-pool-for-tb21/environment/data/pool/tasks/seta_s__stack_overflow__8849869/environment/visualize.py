#!/usr/bin/env python3
"""Overlay detected marker positions on images for visual debugging."""

import sys
import os
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, "/opt/marker_pipeline")
from marker_detector.color import extract_red_channel, compute_white_channel
from marker_detector.kernel import build_stripe_kernel
from marker_detector.detect import convolve_and_find_peaks
from marker_detector.config import KERNEL_H, KERNEL_W, STRIPE_WIDTH, THRESHOLD


def visualize(image_dir, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(image_dir, "debug")
    os.makedirs(output_dir, exist_ok=True)

    for fname in sorted(os.listdir(image_dir)):
        if not fname.endswith(".png"):
            continue
        img = np.array(Image.open(os.path.join(image_dir, fname)))
        red = extract_red_channel(img)
        white = compute_white_channel(img)
        kernel = build_stripe_kernel(KERNEL_H, KERNEL_W, STRIPE_WIDTH)
        markers = convolve_and_find_peaks(red, white, kernel, THRESHOLD)

        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)
        for m in markers:
            cx, cy = m["x"], m["y"]
            draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline="lime", width=2)
            draw.text((cx + 10, cy - 5), f"({cx},{cy})", fill="lime")

        out_path = os.path.join(output_dir, f"debug_{fname}")
        pil_img.save(out_path)
        print(f"Saved {out_path} with {len(markers)} markers")


if __name__ == "__main__":
    image_dir = sys.argv[1] if len(sys.argv) > 1 else "/opt/marker_pipeline/images"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    visualize(image_dir, output_dir)
