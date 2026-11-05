#!/usr/bin/env python3
"""Install tmux and uv without curl/wget using only Python stdlib."""
import urllib.request
import subprocess
import os
import tarfile
import shutil

# === Install tmux via apt with workaround for disk space ===
# Clean apt caches first
for d in ["/var/cache/apt/archives", "/var/lib/apt/lists"]:
    if os.path.isdir(d):
        for f in os.listdir(d):
            fp = os.path.join(d, f)
            if os.path.isfile(fp) and f != "lock":
                os.remove(fp)

os.makedirs("/var/cache/apt/archives/partial", exist_ok=True)

subprocess.run(
    ["apt-get", "update", "-o", "Acquire::Languages=none",
     "-o", "Acquire::GzipIndexes=true",
     "-o", "Acquire::CompressionTypes::Order::=gz"],
    check=False
)

r = subprocess.run(
    ["apt-get", "install", "-y", "--no-install-recommends",
     "-o", "Dir::Cache::Archives=/tmp", "tmux"],
    capture_output=True, text=True
)
if r.returncode != 0:
    print("apt install output:", r.stdout[-300:])
    print("apt install errors:", r.stderr[-300:])
    # Fallback: download debs directly
    os.makedirs("/tmp/debs", exist_ok=True)
    subprocess.run(
        ["apt-get", "download", "tmux", "libevent-core-2.1-7t64", "libjemalloc2"],
        cwd="/tmp/debs", capture_output=True, text=True
    )
    for f in sorted(os.listdir("/tmp/debs")):
        if f.endswith(".deb"):
            subprocess.run(["dpkg", "-i", f"/tmp/debs/{f}"], check=False)
    shutil.rmtree("/tmp/debs", ignore_errors=True)

# Clean up apt lists to save space
shutil.rmtree("/var/lib/apt/lists", ignore_errors=True)
os.makedirs("/var/lib/apt/lists/partial", exist_ok=True)

assert shutil.which("tmux"), "tmux installation failed"
print(f"tmux installed at: {shutil.which('tmux')}")

# === Install uv directly (no curl needed) ===
uv_url = "https://github.com/astral-sh/uv/releases/download/0.10.11/uv-x86_64-unknown-linux-gnu.tar.gz"
uv_tar = "/tmp/uv.tar.gz"

print(f"Downloading uv from {uv_url}")
urllib.request.urlretrieve(uv_url, uv_tar)

os.makedirs(os.path.expanduser("~/.local/bin"), exist_ok=True)

with tarfile.open(uv_tar, "r:gz") as tar:
    tar.extractall("/tmp/uv_extract")

# Find uv binary in extracted files
for root, dirs, files in os.walk("/tmp/uv_extract"):
    for f in files:
        if f in ("uv", "uvx"):
            src = os.path.join(root, f)
            dst = os.path.expanduser(f"~/.local/bin/{f}")
            shutil.copy2(src, dst)
            os.chmod(dst, 0o755)

os.remove(uv_tar)
shutil.rmtree("/tmp/uv_extract", ignore_errors=True)

# Create env file for sourcing
env_dir = os.path.expanduser("~/.local/bin")
env_file = os.path.expanduser("~/.local/bin/env")
with open(env_file, "w") as f:
    f.write(f'export PATH="{env_dir}:$PATH"\n')

assert shutil.which("uv") or os.path.exists(os.path.expanduser("~/.local/bin/uv")), "uv installation failed"
print(f"uv installed at: {os.path.expanduser('~/.local/bin/uv')}")
print("All dependencies installed successfully")
