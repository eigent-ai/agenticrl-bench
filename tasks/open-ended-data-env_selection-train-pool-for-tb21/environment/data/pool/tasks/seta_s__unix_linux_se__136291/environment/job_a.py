#!/usr/bin/env python3
import time
import signal

signal.signal(signal.SIGTERM, lambda s, f: exit(0))
while True:
    time.sleep(1)
