"""Parse Android logcat-style log files."""

import os
import re


def parse_file(filepath):
    """Parse a single logcat log file and extract structured entries."""
    entries = []
    pattern = r"D/(\w+)\s*\(.*\): (.*)"
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(pattern, line)
            if m:
                entries.append({
                    "level": "D",
                    "component": m.group(1),
                    "message": m.group(2)
                })
    return entries


def parse_logs(log_dir):
    """Parse all log files in a directory."""
    all_entries = {}
    for fname in sorted(os.listdir(log_dir)):
        if fname.endswith(".log"):
            device_id = fname.replace(".log", "")
            all_entries[device_id] = parse_file(os.path.join(log_dir, fname))
    return all_entries
