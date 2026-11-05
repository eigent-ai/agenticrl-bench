#!/bin/bash
echo "=== /var/tmp Disk Usage ==="
df -h /var/tmp
echo ""
echo "=== Swap Files in /var/tmp ==="
find /var/tmp -maxdepth 1 -name ".*.swp" -ls 2>/dev/null
echo ""
COUNT=$(find /var/tmp -maxdepth 1 -name ".*.swp" 2>/dev/null | wc -l)
echo "Total: ${COUNT} swap file(s) found"
