#!/usr/bin/env python3
"""jboss-admin-console - Simulated JBoss Admin Console"""
import mmap, time, os
with open("/var/run/jboss-admin-console.pid", "w") as f:
    f.write(str(os.getpid()))
mm = mmap.mmap(-1, 50 * 1024 * 1024)
while True:
    time.sleep(3600)
