#!/usr/bin/env python3
"""
Analyse colour pairs from colors.csv and print their WCAG contrast ratios.
"""
import csv
import sys
from color_utils import hex_to_rgb, relative_luminance, wcag_contrast_ratio


def compute_contrast(hex1, hex2):
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)
    Y1 = relative_luminance(r1, g1, b1)
    Y2 = relative_luminance(r2, g2, b2)
    return wcag_contrast_ratio(Y1, Y2)


def main():
    csv_path = 'colors.csv'
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c1 = row['color1'].strip()
            c2 = row['color2'].strip()
            ratio = compute_contrast(c1, c2)
            print(f"{c1} / {c2}: {ratio:.4f}:1")


if __name__ == '__main__':
    main()
