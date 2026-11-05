#!/bin/bash
FLEET_DIR="/opt/procfleet"
CONF="$FLEET_DIR/config/fleet.conf"

echo "=== Fleet Status Report ==="
echo "Timestamp: $(date)"
echo ""
echo "--- Worker Status ---"

total_workers=0

while IFS=: read -r worker_name count max_rss; do
    [[ "$worker_name" =~ ^# ]] && continue
    [ -z "$worker_name" ] && continue

    running=$(ps aux | grep "${worker_name}.sh" | wc -l)
    total_workers=$((total_workers + running))

    echo "${worker_name}: running=${running} expected=${count}"
done < "$CONF"

echo ""
echo "--- System Health ---"

zombie_count=$(ps aux | grep "Z" | grep -v grep | wc -l)
echo "Zombie processes: ${zombie_count}"
echo "Total fleet workers: ${total_workers}"
