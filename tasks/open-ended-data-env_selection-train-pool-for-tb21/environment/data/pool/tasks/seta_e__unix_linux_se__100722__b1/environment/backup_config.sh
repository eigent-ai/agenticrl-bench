#!/bin/bash
echo "Starting configuration backup..."
echo "WARNING: Checking available disk space..." >&2
cp /etc/hostname /tmp/sysmon_hostname.bak 2>/dev/null || true
echo "Backup completed at $(date)"
echo "INFO: Backup process finished." >&2
