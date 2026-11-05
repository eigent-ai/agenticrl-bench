#!/bin/bash
mkdir -p /mnt/nfs-bench-target
mount -t tmpfs -o size=256m tmpfs /mnt/nfs-bench-target 2>/dev/null || true
exec "$@"
