#!/bin/bash

cat > /app/pkg_audit.py << 'PYEOF'
#!/usr/bin/env python3
"""Package Repository Auditing Tool."""

import sys
import subprocess
import json
import re


def get_package_info(package_name):
    info = {
        "package": package_name,
        "version": None,
        "repository": None,
        "archive_url": None,
        "distribution": None,
        "component": None,
        "error": None
    }

    # Check if package is installed via dpkg -s
    try:
        dpkg_result = subprocess.run(
            ["dpkg", "-s", package_name],
            capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        info["error"] = f"Timeout querying {package_name}"
        return info

    if dpkg_result.returncode != 0:
        info["error"] = f"Package {package_name} is not installed"
        return info

    # Extract version from dpkg output
    for line in dpkg_result.stdout.split('\n'):
        if line.startswith('Version:'):
            info["version"] = line.split(':', 1)[1].strip()
            break

    # Get repository info via apt-cache policy
    try:
        policy_result = subprocess.run(
            ["apt-cache", "policy", package_name],
            capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        info["repository"] = "locally-installed"
        return info

    if policy_result.returncode == 0:
        lines = policy_result.stdout.split('\n')
        for i, line in enumerate(lines):
            if '***' in line:
                # Next line has the repo info
                if i + 1 < len(lines):
                    repo_line = lines[i + 1].strip()
                    info["repository"] = repo_line

                    if 'ppa.launchpad.net' in repo_line or 'ppa.launchpadcontent.net' in repo_line:
                        # PPA detection
                        match = re.search(r'ppa\.launchpad(?:content)?\.net/([^/]+/[^/]+)', repo_line)
                        if match:
                            info["archive_url"] = f"ppa:{match.group(1)}"
                        else:
                            info["archive_url"] = "PPA"
                        info["distribution"] = "PPA"
                        # Try to extract component
                        parts = repo_line.split()
                        for part in parts:
                            if '/' in part and not part.startswith('http'):
                                dist_comp = part
                                if '/' in dist_comp:
                                    _, comp = dist_comp.split('/', 1)
                                    info["component"] = comp
                                break
                    else:
                        # Regular repository
                        parts = repo_line.split()
                        if len(parts) >= 2:
                            # Skip the priority number
                            url_idx = 0
                            for idx, p in enumerate(parts):
                                if p.startswith('http'):
                                    url_idx = idx
                                    break
                            if parts[url_idx].startswith('http'):
                                info["archive_url"] = parts[url_idx]
                                if url_idx + 1 < len(parts):
                                    dist_comp = parts[url_idx + 1]
                                    if '/' in dist_comp:
                                        dist, comp = dist_comp.split('/', 1)
                                        info["distribution"] = dist
                                        info["component"] = comp
                                    else:
                                        info["distribution"] = dist_comp
                break

    # If no repository found, mark as locally-installed
    if not info["repository"]:
        info["repository"] = "locally-installed"

    return info


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No package names provided"}))
        sys.exit(1)

    packages = sys.argv[1:]
    results = {}
    for pkg in packages:
        results[pkg] = get_package_info(pkg)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
PYEOF

chmod +x /app/pkg_audit.py

echo "Done!"
