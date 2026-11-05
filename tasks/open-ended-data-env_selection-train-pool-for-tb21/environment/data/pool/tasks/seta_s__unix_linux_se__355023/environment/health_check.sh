#!/bin/bash
set -e
REPORT="/var/log/health_check.log"
mkdir -p /var/log

exec > "$REPORT" 2>&1

echo "=== System Health Check Report ==="
echo "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
echo ""

echo "--- NFS Export Query ---"
timeout 5 showmount -e localhost || true

echo ""
echo "--- ARP Cache ---"
arp -n

echo ""
echo "--- I/O Statistics ---"
iostat -c 1 1

echo ""
echo "--- System Status ---"
sysping

echo ""
echo "=== Report Complete ==="
