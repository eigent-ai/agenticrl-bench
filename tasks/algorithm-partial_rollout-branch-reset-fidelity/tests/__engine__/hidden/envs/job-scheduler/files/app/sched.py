#!/usr/bin/env python3
"""Job scheduler helper."""
import argparse
import datetime
import json

JOBS = ["rotate-logs", "sync-users", "rebuild-index"]
ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
p = sub.add_parser("plan")
p.add_argument("--exact", action="store_true", help="next_run exactly 24h from now")
s = sub.add_parser("show")
s.add_argument("--date", required=True)
a = ap.parse_args()
if a.cmd == "plan":
    today = datetime.date.today()
    if a.exact:
        nxt = (datetime.datetime.now() + datetime.timedelta(hours=24)).isoformat()
    else:
        nxt = (today + datetime.timedelta(days=1)).isoformat()
    with open("schedule.json", "w") as f:
        json.dump({"day": today.isoformat(), "next_run": nxt, "jobs": JOBS}, f, indent=1)
    print("planned", len(JOBS), "jobs")
else:
    d = datetime.date.fromisoformat(a.date)
    for i, j in enumerate(JOBS):
        print(d + datetime.timedelta(days=i), j)
