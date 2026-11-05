#!/usr/bin/env python3
"""
session_report.py - Generate a report of forced user logouts.
Reads the session manager log and summarizes logout events.
"""

import re
import sys
from collections import defaultdict

LOG_FILE = "/var/log/session-mgr/session.log"

# Parse log entries of the form:
# 2024-01-15 14:30:22 LOGOUT user=alice uid=1001 procs=3
LOG_PATTERN = re.compile(
    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+user:(\w+)\s+uid:(\d+)\s+procs:(\d+)$'
)


def parse_log(path):
    events = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                m = LOG_PATTERN.match(line)
                if m:
                    events.append({
                        'timestamp': m.group(1),
                        'action':    m.group(2),
                        'user':      m.group(3),
                        'uid':       int(m.group(4)),
                        'procs':     int(m.group(5)),
                    })
    except FileNotFoundError:
        print(f"ERROR: Log file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return events


def generate_report(events):
    if not events:
        print("No logout events found in log.")
        return

    user_stats = defaultdict(lambda: {'count': 0, 'procs': 0})
    for e in events:
        user_stats[e['user']]['count'] += 1
        user_stats[e['user']]['procs'] += e['procs']

    total_events = len(events)
    total_procs  = sum(s['procs'] for s in user_stats.values())

    print("=== Session Logout Report ===")
    print(f"Total logout events : {total_events}")
    print(f"Total processes killed: {total_procs}")
    print("Per-user summary:")
    for user in sorted(user_stats):
        s = user_stats[user]
        print(f"  {user}: {s['count']} logout(s), {s['procs']} process(es) killed")


if __name__ == '__main__':
    events = parse_log(LOG_FILE)
    generate_report(events)
