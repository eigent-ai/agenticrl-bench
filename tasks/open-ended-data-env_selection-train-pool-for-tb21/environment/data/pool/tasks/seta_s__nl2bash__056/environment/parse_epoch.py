#!/usr/bin/env python3
import sys
import datetime

s = sys.stdin.read().strip()
dt = datetime.datetime.strptime(s, "%b %d %H:%M:%S %Y %Z")
dt = dt.replace(tzinfo=datetime.timezone.utc)
print(int(dt.timestamp()))
