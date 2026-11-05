#!/usr/bin/env python3
"""Optimization benchmarking pipeline.

Runs multiple global optimization algorithms against standard mathematical
test functions and produces a JSON results report.
"""

import json
import os
import sys

from config import ALGORITHMS, validate_bounds
from benchmark import TEST_FUNCTIONS
from results_collector import record_result, get_all_results


def run_single_benchmark(algo_name, algo_func, func_info):
    """Run a single optimization benchmark."""
    bounds = func_info["bounds"]
    validate_bounds(bounds)

    result = algo_func(func_info["func"], bounds=bounds, seed=42)

    return {
        "algorithm": algo_name,
        "function": func_info["name"],
        "best_value": float(result.fun),
        "num_evaluations": int(result.nfev),
        "success": bool(result.success)
    }


def main():
    """Run all benchmarks and produce report."""
    os.makedirs("/opt/optbench/results", exist_ok=True)

    errors = []
    for algo_name, algo_func in ALGORITHMS.items():
        for func_info in TEST_FUNCTIONS:
            try:
                result = run_single_benchmark(algo_name, algo_func, func_info)
                record_result(algo_name, func_info["name"], result)
                print(f"OK: {algo_name} on {func_info['name']} -> {result['best_value']:.6f}")
            except Exception as e:
                errors.append(f"{algo_name}/{func_info['name']}: {e}")
                print(f"FAIL: {algo_name} on {func_info['name']}: {e}")

    all_results = get_all_results()

    report_path = "/opt/optbench/results/benchmark_report.json"
    with open(report_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults written to {report_path}")

    if errors:
        print(f"\n{len(errors)} benchmark(s) failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print(f"All {len(all_results)} benchmarks completed successfully.")
    return 0


if __name__ == "__main__":
    main()
