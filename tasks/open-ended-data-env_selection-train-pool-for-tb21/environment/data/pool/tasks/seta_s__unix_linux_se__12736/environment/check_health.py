#!/usr/bin/env python
import datetime
import os

status_file = "/opt/monitor/data/health_status"
print(f"OK - System healthy at {datetime.datetime.now().isoformat()}")
with open(status_file, "w") as f:
    f.write("healthy\n")
