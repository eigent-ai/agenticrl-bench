#!/usr/bin/env python3
"""Blind Source Separation Pipeline

Reads mixed audio signals from CSV, applies SVD-based blind source separation,
and writes the recovered source signals to output files.
"""
import sys
import os
import yaml
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from src.io_utils import load_csv, save_csv
from src.preprocess import center_and_whiten
from src.separation import separate_sources


def main():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    data_dir = config["data_dir"]
    output_dir = config["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    mixed_path = os.path.join(data_dir, "mixed.csv")
    print(f"Loading mixed signals from {mixed_path}")
    mixed = load_csv(mixed_path)
    print(f"Mixed signal shape: {mixed.shape}")

    print("Preprocessing: centering and whitening...")
    whitened = center_and_whiten(mixed)
    print(f"Whitened signal shape: {whitened.shape}")

    print("Separating sources via SVD...")
    separated = separate_sources(whitened)
    print(f"Separated signal shape: {separated.shape}")

    for i in range(separated.shape[1]):
        out_path = os.path.join(output_dir, f"source_{i+1}.csv")
        save_csv(out_path, separated[:, i:i+1])
        print(f"Wrote recovered source {i+1} to {out_path}")

    print("Pipeline complete.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Pipeline failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
