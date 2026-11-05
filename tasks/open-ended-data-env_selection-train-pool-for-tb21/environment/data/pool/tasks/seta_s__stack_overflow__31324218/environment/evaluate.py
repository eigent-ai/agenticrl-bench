#!/usr/bin/env python3
"""Classification metrics evaluation pipeline.

Reads confusion matrices from data/, computes per-class and aggregated
metrics, and writes a JSON report to output/report.json.
"""

import json
import os

import numpy as np

from metrics.confusion import extract_per_class_metrics
from metrics.derived import compute_sensitivity, compute_specificity, compute_precision, compute_f1
from metrics.aggregate import macro_average, weighted_average


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def load_confusion_matrix(filepath):
    """Load a confusion matrix from a CSV file."""
    return np.loadtxt(filepath, delimiter=',', dtype=int)


def evaluate_dataset(cm):
    """Evaluate a single confusion matrix and return metrics dict."""
    per_class_raw = extract_per_class_metrics(cm)
    per_class_results = []

    for entry in per_class_raw:
        tp = entry["TP"]
        fp = entry["FP"]
        tn = entry["TN"]
        fn = entry["FN"]

        sens = compute_sensitivity(tp, fp, tn, fn)
        spec = compute_specificity(tp, fp, tn, fn)
        prec = compute_precision(tp, fp, tn, fn)
        f1 = compute_f1(prec, sens)

        per_class_results.append({
            "class": entry["class"],
            "TP": tp,
            "FP": fp,
            "TN": tn,
            "FN": fn,
            "sensitivity": round(sens, 4),
            "specificity": round(spec, 4),
            "precision": round(prec, 4),
            "f1": round(f1, 4),
        })

    macro_avg = macro_average(per_class_results)
    weighted_avg = weighted_average(per_class_results)

    return {
        "per_class": per_class_results,
        "macro_avg": {k: round(v, 4) for k, v in macro_avg.items()},
        "weighted_avg": {k: round(v, 4) for k, v in weighted_avg.items()},
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report = {}

    for filename in sorted(os.listdir(DATA_DIR)):
        if filename.endswith(".tsv"):
            dataset_name = filename.replace(".tsv", "")
            filepath = os.path.join(DATA_DIR, filename)
            cm = load_confusion_matrix(filepath)
            report[dataset_name] = evaluate_dataset(cm)

    output_path = os.path.join(OUTPUT_DIR, "report.json")
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
