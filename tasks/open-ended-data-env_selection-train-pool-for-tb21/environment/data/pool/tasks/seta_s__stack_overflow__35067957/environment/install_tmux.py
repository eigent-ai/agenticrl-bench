#!/usr/bin/env python3
"""Download and install tmux without apt to avoid disk space issues."""
import urllib.request
import subprocess
import os
import json

def get_pkg_url(pkg_name):
    """Find the correct URL for a trixie package."""
    # Use the Debian API to find exact package URLs
    url = f"https://sources.debian.org/api/src/{pkg_name}/"
    # Fallback: just try to install via dpkg from snapshot
    return None

# First try apt with aggressive space saving
# Clean everything first
for d in ["/var/cache/apt/archives", "/var/lib/apt/lists", "/var/cache/apt/pkgcache.bin", "/var/cache/apt/srcpkgcache.bin"]:
    if os.path.isfile(d):
        os.remove(d)
    elif os.path.isdir(d):
        for f in os.listdir(d):
            fp = os.path.join(d, f)
            if os.path.isfile(fp) and f != "lock":
                os.remove(fp)

os.makedirs("/var/cache/apt/archives/partial", exist_ok=True)

# Use apt-get with minimal lists - only download what we need
r = subprocess.run(
    ["apt-get", "update", "-o", "Acquire::Languages=none",
     "-o", "Acquire::GzipIndexes=true", "-o", "Acquire::CompressionTypes::Order::=gz"],
    capture_output=True, text=True
)
print(r.stdout[-500:] if len(r.stdout) > 500 else r.stdout)
if r.returncode != 0:
    print("apt-get update stderr:", r.stderr[-500:])

# Try installing with download to /tmp
r = subprocess.run(
    ["apt-get", "install", "-y", "--no-install-recommends",
     "-o", "Dir::Cache::Archives=/tmp",
     "tmux"],
    capture_output=True, text=True
)
print(r.stdout[-500:] if len(r.stdout) > 500 else r.stdout)
if r.returncode != 0:
    print("Install stderr:", r.stderr[-500:])
    # Try dpkg direct approach
    print("Trying direct dpkg approach...")
    # Get tmux via apt-get download
    os.makedirs("/tmp/debs", exist_ok=True)
    subprocess.run(
        ["apt-get", "download", "-o", "Dir::Cache::Archives=/tmp/debs", "tmux", "libevent-core-2.1-7t64", "libjemalloc2"],
        cwd="/tmp/debs", capture_output=True, text=True
    )
    for f in os.listdir("/tmp/debs"):
        if f.endswith(".deb"):
            subprocess.run(["dpkg", "-i", f"/tmp/debs/{f}"], check=False)
    subprocess.run(["rm", "-rf", "/tmp/debs"])

# Verify
r = subprocess.run(["which", "tmux"], capture_output=True, text=True)
if r.returncode == 0:
    print(f"tmux installed at: {r.stdout.strip()}")
else:
    print("WARNING: tmux not found after installation attempts")
    raise SystemExit(1)
