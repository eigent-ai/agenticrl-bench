#!/usr/bin/env python3
"""Entry point: loads data, runs fitting, writes report."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fitting.pipeline import load_data, fit_distributions
from fitting.report import generate_report

def main():
    data_path = os.path.join(os.path.dirname(__file__), "data", "observations.csv")
    output_path = os.path.join(os.path.dirname(__file__), "output", "fit_report.json")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("Loading observation data...")
    expanded_data = load_data(data_path)
    print(f"Loaded {len(expanded_data)} observations")

    print("Fitting distributions...")
    fit_results = fit_distributions(expanded_data)
    print(f"Fitted {len(fit_results)} distributions")

    print("Generating report...")
    generate_report(fit_results, expanded_data, output_path)
    print(f"Report written to {output_path}")

if __name__ == "__main__":
    main()
