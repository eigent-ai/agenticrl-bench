#!/usr/bin/env python3
"""jboss-web-01 - Simulated JBoss Web Server Instance 1"""
import mmap, time, os
with open("/var/run/jboss-web-01.pid", "w") as f:
    f.write(str(os.getpid()))
mm = mmap.mmap(-1, 200 * 1024 * 1024)
while True:
    time.sleep(3600)
