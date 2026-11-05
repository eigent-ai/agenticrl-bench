#!/usr/bin/env python3
"""Pipeline orchestrator: runs extract, transform, and report stages in sequence."""

import sys
import traceback

from extract import extract
from transform import transform
from report import generate_report


def main():
    stages = [
        ("extract", extract),
        ("transform", transform),
        ("report", generate_report),
    ]

    for name, func in stages:
        print(f"Running stage: {name}")
        try:
            func()
        except Exception as e:
            print(f"Stage '{name}' failed with error: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)
        print(f"Stage '{name}' completed successfully")

    print("Pipeline finished successfully")


if __name__ == "__main__":
    main()
