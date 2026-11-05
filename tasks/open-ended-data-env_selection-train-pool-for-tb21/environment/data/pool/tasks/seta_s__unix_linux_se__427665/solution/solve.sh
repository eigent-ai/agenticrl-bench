#!/bin/bash
set -e

# Step 1: Install the staged packages.
# docker-buildx-plugin must be installed before docker-ce (dependency ordering).
dpkg -i /opt/docker-pkgs/docker-buildx-plugin_*.deb || true
dpkg -i /opt/docker-pkgs/docker-ce_*.deb || true

# Step 2: Remove the broken socket unit override that references a non-existent group.
# The correct socket unit is now at /lib/systemd/system/docker.socket (from docker-ce).
rm -f /etc/systemd/system/docker.socket

# Step 3: Fix the dangling socket enable symlink.
# The docker-ce post-install script ran "systemctl enable docker.socket" which created:
#   /etc/systemd/system/sockets.target.wants/docker.socket -> /etc/systemd/system/docker.socket
# That target was the broken override we just removed, leaving a dangling symlink.
# Replace it with one pointing to the package-installed socket unit.
rm -f /etc/systemd/system/sockets.target.wants/docker.socket
mkdir -p /etc/systemd/system/sockets.target.wants
ln -s /lib/systemd/system/docker.socket \
    /etc/systemd/system/sockets.target.wants/docker.socket

# Step 4: If a live systemd is accessible, reload and enable+start Docker.
# In some environments systemd is not the init; skip gracefully in that case.
if systemctl is-system-running 2>/dev/null | grep -qE 'running|degraded|initializing|starting'; then
    systemctl daemon-reload
    systemctl enable docker
    systemctl start docker
    timeout 30 bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done' || true
fi
