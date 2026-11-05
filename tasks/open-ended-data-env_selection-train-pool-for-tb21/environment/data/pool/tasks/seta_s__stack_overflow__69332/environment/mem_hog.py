#!/usr/bin/env python3
"""Memory and CPU consuming workload."""
import time

# Allocate ~32MB of memory
data = [bytearray(1024 * 1024) for _ in range(32)]

# CPU work loop
while True:
    total = 0
    for i in range(200000):
        total += i * i
    time.sleep(0.05)
