#!/usr/bin/env python3
"""jboss-worker-02 - Simulated JBoss Worker Instance 2"""
import mmap, time, os
with open("/var/run/jboss-worker-02.pid", "w") as f:
    f.write(str(os.getpid()))
mm = mmap.mmap(-1, 300 * 1024 * 1024)
while True:
    time.sleep(3600)
