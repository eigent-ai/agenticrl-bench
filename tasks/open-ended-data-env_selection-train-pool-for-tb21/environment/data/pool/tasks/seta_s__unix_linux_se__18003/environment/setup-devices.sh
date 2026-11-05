#!/bin/bash
# setup-devices.sh - Create device nodes for X11 container
# Run with --dry-run to preview commands without executing

set -euo pipefail

CONTAINER_ROOT="${CONTAINER_ROOT:-/var/lib/lxc/desktop-worker/rootfs}"
DRY_RUN=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --help) echo "Usage: $0 [--dry-run] [--help]"; exit 0 ;;
    esac
done

run_cmd() {
    if $DRY_RUN; then
        echo "$@"
    else
        "$@"
    fi
}

echo "Setting up device nodes for container desktop-worker"

# TTY device for virtual terminal 10
run_cmd mknod -m 620 "${CONTAINER_ROOT}/dev/tty10" c 5 10
run_cmd chown root:tty "${CONTAINER_ROOT}/dev/tty10"

# NVIDIA GPU device 0
run_cmd mknod -m 644 "${CONTAINER_ROOT}/dev/nvidia0" c 195 0
run_cmd chown root:video "${CONTAINER_ROOT}/dev/nvidia0"

# NVIDIA control device
run_cmd mknod -m 666 "${CONTAINER_ROOT}/dev/nvidiactl" c 195 0
run_cmd chown root:video "${CONTAINER_ROOT}/dev/nvidiactl"

# NVIDIA UVM device
run_cmd mknod -m 666 "${CONTAINER_ROOT}/dev/nvidia-uvm" c 195 1
run_cmd chown root:video "${CONTAINER_ROOT}/dev/nvidia-uvm"

# DRI render nodes
run_cmd mknod -m 666 "${CONTAINER_ROOT}/dev/dri/card0" c 226 0
run_cmd mknod -m 666 "${CONTAINER_ROOT}/dev/dri/renderD128" c 226 128

# Bind-mount X11 socket directory into container
run_cmd mount --bind /tmp/.X11-unix "${CONTAINER_ROOT}/tmp/.X11-unix"

echo "Device setup complete"
