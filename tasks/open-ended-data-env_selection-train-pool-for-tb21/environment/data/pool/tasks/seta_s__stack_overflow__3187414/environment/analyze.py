#!/usr/bin/env python3
"""Analyze benchmark timings and produce a comparison report."""

import csv
import json
import sys

def main():
    csv_path = "output/timings.csv"
    report_path = "output/report.json"

    timings = {}
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 4:
                continue
            # Parse columns: compiler, opt, benchmark, time
            compiler = row[0]
            opt = row[1]
            benchmark = row[2]
            time_val = float(row[3])
            key = (benchmark, opt)
            if key not in timings:
                timings[key] = {}
            timings[key][compiler] = time_val

    report = []
    for (benchmark, opt), data in sorted(timings.items()):
        gcc_time = data.get("gcc", 0.0)
        clang_time = data.get("clang", 0.0)
        if gcc_time > 0 and clang_time > 0:
            speedup = clang_time / gcc_time
        else:
            speedup = 0.0
        report.append({
            "benchmark": benchmark,
            "opt_level": opt,
            "gcc_time": gcc_time,
            "clang_time": clang_time,
            "gcc_speedup_over_clang": round(speedup, 4)
        })

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to {report_path}")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
