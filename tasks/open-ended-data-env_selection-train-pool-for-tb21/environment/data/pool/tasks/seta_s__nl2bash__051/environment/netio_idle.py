#!/usr/bin/env python3
import time, os

PID_FILE = "/opt/netio_sim/netio_idle.pid"
BYTES_FILE = "/opt/netio_sim/netio_idle.bytes"

with open(PID_FILE, "w") as f:
    f.write(str(os.getpid()))

with open(BYTES_FILE, "w") as f:
    f.write("0")

while True:
    time.sleep(60)
