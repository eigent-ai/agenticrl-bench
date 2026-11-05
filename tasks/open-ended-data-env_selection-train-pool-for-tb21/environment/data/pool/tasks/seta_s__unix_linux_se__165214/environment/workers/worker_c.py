#!/usr/bin/env python3
"""Worker C - periodic logging task."""
import time
import os

counter = 0
while True:
    counter += 1
    _ = os.getpid()
    time.sleep(30)
