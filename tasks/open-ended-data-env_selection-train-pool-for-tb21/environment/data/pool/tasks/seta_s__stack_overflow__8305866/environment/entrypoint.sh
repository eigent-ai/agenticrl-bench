#!/bin/bash
# Attempt to configure core dump destination (requires SYS_ADMIN capability)
echo "core.%p" > /proc/sys/kernel/core_pattern 2>/dev/null || true
exec "$@"
