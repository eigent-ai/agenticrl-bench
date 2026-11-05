#!/usr/bin/env python
# utils.py - Utility script
import sys

def check_environment():
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version}")
    return 0

if __name__ == "__main__":
    exit(check_environment())
