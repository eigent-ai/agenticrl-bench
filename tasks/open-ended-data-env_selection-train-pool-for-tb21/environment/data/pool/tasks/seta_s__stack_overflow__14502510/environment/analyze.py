#!/usr/bin/env python3
"""Analyze simulation results."""
import csv
import sys
import statistics

def main():
    if len(sys.argv) != 2:
        print("Usage: analyze.py <results_dir>")
        sys.exit(1)

    csv_path = f"{sys.argv[1]}/output.csv"
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        values = [float(row["value"]) for row in reader]

    print(f"Steps: {len(values)}")
    print(f"Mean: {statistics.mean(values):.6f}")
    print(f"Stdev: {statistics.stdev(values):.6f}")
    print(f"Min: {min(values):.6f}")
    print(f"Max: {max(values):.6f}")

if __name__ == "__main__":
    main()
