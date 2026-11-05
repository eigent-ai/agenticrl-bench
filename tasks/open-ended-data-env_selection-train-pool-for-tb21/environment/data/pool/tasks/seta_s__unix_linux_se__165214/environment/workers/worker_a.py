#!/usr/bin/env python3
"""Worker A - periodic computation task."""
import time
import math

counter = 0
while True:
    counter += 1
    _ = math.factorial(50)
    time.sleep(30)
