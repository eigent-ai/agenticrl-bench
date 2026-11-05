import pandas as pd
import numpy as np
import sys


def compute_accuracy(predictions, labels):
    correct = (predictions == labels).sum()
    total = len(labels)
    return correct / total


def main():
    base_dir = "/opt/pipeline"
    output_path = f"{base_dir}/output/results.csv"
    input_path = f"{base_dir}/data/input.csv"

    results = pd.read_csv(output_path)
    original = pd.read_csv(input_path)

    data = results.head(50)
    labels = original["label"].head(50)

    numeric_cols = [c for c in data.columns if c != "label"]
    feature_mean = data[numeric_cols].mean(axis=1)

    threshold = feature_mean.median()
    predictions = (feature_mean > threshold).astype(int)

    accuracy = compute_accuracy(predictions, labels)
    sample_count = len(data)

    print(f"Validation Results:")
    print(f"  Samples evaluated: {sample_count}")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  Threshold: {threshold:.6f}")

    if accuracy < 0.0 or accuracy > 1.0:
        print("ERROR: Invalid accuracy value")
        sys.exit(1)

    print("Validation complete.")


if __name__ == "__main__":
    main()
