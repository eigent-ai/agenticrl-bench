import os
import sys
import yaml
from preprocess import process_batch
from validate import validate_batches
import numpy as np


def main():
    config_path = "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    raw_dir = "data/raw"
    processed_dir = config["batch_output_dir"]
    os.makedirs(processed_dir, exist_ok=True)

    batch_files = sorted([
        f for f in os.listdir(raw_dir) if f.endswith(".npy")
    ])

    if not batch_files:
        print("No raw batches found.")
        sys.exit(1)

    for batch_file in batch_files:
        raw_path = os.path.join(raw_dir, batch_file)
        print(f"Processing {batch_file}...")
        processed = process_batch(raw_path, config)
        out_path = os.path.join(processed_dir, batch_file)
        np.save(out_path, processed)
        print(f"  Saved to {out_path} with shape {processed.shape}")

    print("\nRunning validation...")
    report = validate_batches(processed_dir, config_path)

    if report["status"] != "pass":
        print("Pipeline FAILED validation:")
        for err in report["errors"]:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("Pipeline completed successfully.")
        print(f"  Total batches: {report['total_batches']}")
        print(f"  Total images: {report['total_images']}")
        sys.exit(0)


if __name__ == "__main__":
    main()
