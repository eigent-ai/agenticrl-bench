#!/usr/bin/env python3
"""Long-running multi-threaded server application."""
import threading
import time

NUM_WORKERS = 5


def worker(n):
    while True:
        time.sleep(1)


for i in range(NUM_WORKERS):
    t = threading.Thread(target=worker, args=(i,), daemon=True)
    t.start()

while True:
    time.sleep(10)
