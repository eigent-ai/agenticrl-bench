#!/usr/bin/env python3
"""jboss-web-02 - Simulated JBoss Web Server Instance 2"""
import mmap, time, os
with open("/var/run/jboss-web-02.pid", "w") as f:
    f.write(str(os.getpid()))
mm = mmap.mmap(-1, 150 * 1024 * 1024)
while True:
    time.sleep(3600)
