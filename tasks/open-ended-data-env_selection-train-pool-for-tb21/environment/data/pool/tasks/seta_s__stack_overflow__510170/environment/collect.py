#!/usr/bin/env python3
"""sysmon — lightweight metrics collector.
Reads config, logs startup, collects /proc metrics, writes a JSON report.
"""
import json
import logging
import os
import time

CONFIG_PATH = "/etc/sysmon/config.json"

# ── 1. Read configuration ──────────────────────────────────────────────────
with open(CONFIG_PATH) as fh:
    config = json.load(fh)

output_dir = config["output_dir"]
log_file   = config["log_file"]

# ── 2. Configure logging ───────────────────────────────────────────────────
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("sysmon")
logger.info("Starting metrics collection (uid=%d)", os.getuid())

# ── 3. Collect metrics ─────────────────────────────────────────────────────
def _read_meminfo():
    info = {}
    with open("/proc/meminfo") as fh:
        for line in fh:
            parts = line.split()
            key = parts[0].rstrip(":")
            if key in ("MemTotal", "MemAvailable", "MemFree"):
                info[key] = int(parts[1])   # kB
    return info

def _read_loadavg():
    with open("/proc/loadavg") as fh:
        return float(fh.read().split()[0])

mem  = _read_meminfo()
load = _read_loadavg()

report = {
    "timestamp":           time.time(),
    "memory_total_kb":     mem.get("MemTotal",     0),
    "memory_available_kb": mem.get("MemAvailable", 0),
    "memory_free_kb":      mem.get("MemFree",      0),
    "load_avg_1min":       load,
    "collector_user":      os.environ.get("USER", f"uid:{os.getuid()}"),
}

# ── 4. Write report ────────────────────────────────────────────────────────
report_path = os.path.join(output_dir, f"report_{int(time.time())}.json")
with open(report_path, "w") as fh:
    json.dump(report, fh, indent=2)

logger.info("Report written to %s", report_path)
print(f"Report written to {report_path}")
