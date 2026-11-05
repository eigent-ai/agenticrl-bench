#!/bin/bash
# firewall-monitor: SSH brute-force detection and mitigation
# Parses /var/log/auth.log, identifies repeat offenders, and blocks them via iptables.

set -euo pipefail

AUTH_LOG="/var/log/auth.log"
AUDIT_LOG="/var/log/firewall-monitor/audit.log"
THRESHOLD=3

if [ ! -f "$AUTH_LOG" ]; then
    echo "ERROR: Auth log not found at $AUTH_LOG" >&2
    exit 1
fi

# Extract IPs with authentication failures and count occurrences
# Build a list of offending IPs sorted by failure count (descending)
declare -A ip_counts

while IFS= read -r line; do
    ip=$(echo "$line" | awk '{print $11}')
    if [ -n "$ip" ]; then
        ip_counts[$ip]=$(( ${ip_counts[$ip]:-0} + 1 ))
    fi
done < <(grep 'authentication failure' "$AUTH_LOG")

blocked_count=0

for ip in "${!ip_counts[@]}"; do
    count=${ip_counts[$ip]}

    if [ "$count" -ge "$THRESHOLD" ]; then
        echo "Blocking $ip ($count failures)"

        # Apply iptables DROP rule for this IP
        iptables -A INPUT -s "$ip" -j DROP

        # Record the action in the audit log
        echo "$ip blocked" >> "$AUDIT_LOG"

        blocked_count=$(( blocked_count + 1 ))
    fi
done

echo "Done. Blocked $blocked_count IP(s)."
exit 0
