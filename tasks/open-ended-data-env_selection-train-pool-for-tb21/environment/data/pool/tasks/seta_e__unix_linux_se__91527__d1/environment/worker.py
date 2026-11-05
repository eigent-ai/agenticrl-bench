#!/usr/bin/env python3
"""Persistent data worker — runs until terminated by SIGTERM."""
import sys
import time
import signal
import os

worker_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
_stop = False


def _on_term(sig, frame):
    global _stop
    _stop = True


signal.signal(signal.SIGTERM, _on_term)

log_path = f"/tmp/workerd_{worker_id}.log"
with open(log_path, "a") as f:
    f.write(f"started pid={os.getpid()}\n")

while not _stop:
    time.sleep(0.5)

with open(log_path, "a") as f:
    f.write(f"stopped pid={os.getpid()}\n")
