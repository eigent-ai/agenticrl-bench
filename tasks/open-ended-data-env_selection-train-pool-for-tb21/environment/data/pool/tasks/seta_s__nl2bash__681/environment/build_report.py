#!/usr/bin/env python3
"""Assemble per-host JSON files into a final health report."""
import json
import sys
import os
import glob
from datetime import datetime, timezone

tmpdir = sys.argv[1]
output_path = sys.argv[2]

hosts = []
for f in sorted(glob.glob(os.path.join(tmpdir, "host_*.json"))):
    with open(f) as fh:
        hosts.append(json.load(fh))

healthy = sum(1 for h in hosts if h.get("packet_loss_pct", 100) == 0)
unreachable = sum(1 for h in hosts if h.get("received", 0) == 0)
degraded = len(hosts) - healthy - unreachable

latencies = [h["avg_latency_ms"] for h in hosts
             if h.get("avg_latency_ms") is not None]
overall_avg = round(sum(latencies) / len(latencies), 3) if latencies else None

report = {
    "hosts": hosts,
    "summary": {
        "total_hosts": len(hosts),
        "healthy_hosts": healthy,
        "degraded_hosts": degraded,
        "unreachable_hosts": unreachable,
        "overall_avg_latency_ms": overall_avg,
    },
    "generated_at": datetime.now(timezone.utc).isoformat(),
}

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump(report, f, indent=2)
