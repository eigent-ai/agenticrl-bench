"""Report generation for benchmark results."""

import csv
import os


def write_report(results, output_path):
    """Write benchmark results to a CSV file.

    Args:
        results: list of dicts with keys: function, iterations, mean_ms, median_ms, p95_ms, p99_ms
        output_path: path to the output CSV file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    headers = ["function", "mean_ms", "median_ms", "p95_ms", "p99_ms"]

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(headers)
        for row in results:
            writer.writerow([
                row["function"],
                f"{row['mean_ms']:.6f}",
                f"{row['median_ms']:.6f}",
                f"{row['p95_ms']:.6f}",
                f"{row['p99_ms']:.6f}",
            ])
