#!/bin/bash
# net-diag.sh - Network diagnostics script for maintenance toolkit

echo "=== Network Diagnostics Report ==="
echo "Date: $(date)"
echo ""

echo "--- IP Addresses ---"
ip addr show 2>/dev/null || echo "ip command not available"
echo ""

echo "--- Listening Ports ---"
ss -tlnp 2>/dev/null || echo "ss command not available"
echo ""

echo "--- Connectivity Test ---"
ping -c 3 localhost 2>/dev/null || echo "ping failed"
echo ""

echo "--- Routing Table ---"
ip route show 2>/dev/null || echo "routing info not available"
echo ""

echo "=== Diagnostics Complete ==="
