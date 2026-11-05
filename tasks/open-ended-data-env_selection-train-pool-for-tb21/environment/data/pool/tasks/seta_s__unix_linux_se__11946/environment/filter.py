#!/usr/bin/env python3
"""Filters log stream, forwarding ERROR and WARN level entries."""
import sys
import re

SEVERITY_PATTERN = re.compile(r'\b(ERROR|WARN)\b')

for line in sys.stdin:
    if SEVERITY_PATTERN.search(line):
        sys.stdout.write(line)
