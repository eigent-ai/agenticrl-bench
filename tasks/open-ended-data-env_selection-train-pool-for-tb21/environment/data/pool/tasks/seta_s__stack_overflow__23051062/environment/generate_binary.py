#!/usr/bin/env python3
"""Generate deterministic binary measurement data."""
import random
import struct
import os

random.seed(42)
os.makedirs("data", exist_ok=True)

with open("data/measurements.dat", "wb") as f:
    for _ in range(50):
        val = random.uniform(0, 100)
        f.write(struct.pack("d", val))
