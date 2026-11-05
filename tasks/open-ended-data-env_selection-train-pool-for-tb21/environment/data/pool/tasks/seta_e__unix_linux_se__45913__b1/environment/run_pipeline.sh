#!/bin/bash
cd /opt/data_pipeline

# Clean any leftover state from previous runs
rm -f /tmp/supervisor.sock /tmp/supervisord.pid
rm -f logs/*.log logs/*.err

# Start supervisord (daemonizes immediately)
supervisord -c supervisord.conf

# Wait for all workers to exit (they finish within a few seconds)
MAX_WAIT=15
ELAPSED=0
while [ $ELAPSED -lt $MAX_WAIT ]; do
    # Check if any worker is still RUNNING
    if ! supervisorctl -c supervisord.conf status 2>/dev/null | grep -q "RUNNING"; then
        break
    fi
    sleep 1
    ELAPSED=$((ELAPSED + 1))
done

# Shut down supervisord
supervisorctl -c supervisord.conf shutdown 2>/dev/null
sleep 1
echo "Pipeline complete"
