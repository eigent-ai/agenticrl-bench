#!/usr/bin/env python3
"""Worker B - periodic data processing task."""
import time
import hashlib

counter = 0
while True:
    counter += 1
    _ = hashlib.sha256(str(counter).encode()).hexdigest()
    time.sleep(30)
