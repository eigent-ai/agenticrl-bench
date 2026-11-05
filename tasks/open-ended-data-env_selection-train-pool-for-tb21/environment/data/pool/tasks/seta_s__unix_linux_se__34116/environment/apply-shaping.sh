#!/bin/bash
set -euo pipefail

source /etc/backup-shaping.conf

# Remove any existing root qdisc on the interface
tc qdisc del dev "$IFACE" root 2>/dev/null || true

# Flush outgoing packet marks
iptables -t mangle -F OUTPUT 2>/dev/null || true

# Root HTB qdisc; default class 10 handles unmarked traffic
tc qdisc add dev "$IFACE" root handle 1: htb default 10

# Class 1:10 — default, full-rate path for normal traffic
tc class add dev "$IFACE" parent 1: classid 1:10 htb rate 1000mbit ceil 1000mbit

# Class 1:20 — rate-limited path for backup traffic
tc class add dev "$IFACE" parent 1: classid 1:20 htb rate "$RATE" ceil "$RATE"

# Route packets carrying the fw mark into the backup class
tc filter add dev "$IFACE" parent 1: handle 2 fw classid 1:20

# Mark all outgoing packets from the backup user
iptables -t mangle -A OUTPUT -m owner --uid-owner "$BACKUP_USER" -j MARK --set-mark "$MARK"
