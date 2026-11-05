#!/bin/bash
FLEET_DIR="/opt/procfleet"
CONF="$FLEET_DIR/config/fleet.conf"

echo "=== Fleet Monitor Report ==="
echo "Timestamp: $(date)"
echo ""

while IFS=: read -r worker_name count max_rss; do
    [[ "$worker_name" =~ ^# ]] && continue
    [ -z "$worker_name" ] && continue

    echo "--- $worker_name (expected: $count, max RSS: ${max_rss}KB) ---"

    pid_list=$(pgrep -f "${worker_name}.sh" | tr "\n" " ")
    pid_list="${pid_list% }"

    if [ -z "$pid_list" ]; then
        echo "  No running instances found"
        echo ""
        continue
    fi

    ps -p $(echo $pid_list | tr ' ' ',') -o pid,user,pcpu,pmem,rss,comm 2>/dev/null | \
        awk '{printf "  PID=%s USER=%s CPU=%s%% MEM=%s%% RSS=%sKB CMD=%s\n", $1, $2, $3, $4, $5, $6}'

    echo ""
done < "$CONF"
