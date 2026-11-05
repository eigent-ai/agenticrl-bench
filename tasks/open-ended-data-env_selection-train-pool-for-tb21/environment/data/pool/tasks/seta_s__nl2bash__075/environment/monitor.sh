#!/bin/bash
# UDP connection monitor for root processes
LOG="/var/log/udp_alerts.log"
ALLOWLIST="/opt/udp_monitor/allowlist.conf"

connections="$(netstat -nup 2>/dev/null | grep -vE '^(Active|Proto)' | awk '{print $6}' | cut -d/ -f1 | sort -u)"

for ip in $connections; do
    if ! grep -qF "$ip" "$ALLOWLIST"; then
        echo "UNAUTHORIZED UDP $ip" | mail -s "Alert" root
    fi
done
