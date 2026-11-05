#!/usr/bin/env python3
"""jboss-worker-01 - Simulated JBoss Worker Instance 1"""
import mmap, time, os
with open("/var/run/jboss-worker-01.pid", "w") as f:
    f.write(str(os.getpid()))
mm = mmap.mmap(-1, 500 * 1024 * 1024)
while True:
    time.sleep(3600)
