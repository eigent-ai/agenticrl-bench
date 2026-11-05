#!/bin/bash
# Verifies that the SSH agent is running with the deployment key loaded.

SSH_ENV="/root/.ssh/environment"
STATUS_FILE="/tmp/agent-status.txt"

if [ ! -f "$SSH_ENV" ]; then
    echo "Error: Agent environment file not found. Run init-agent.sh first." >&2
    exit 1
fi

# Connect to the running agent
SSH_AUTH_SOCK=/var/run/ssh-agent.sock
SSH_AGENT_PID=$(cat /var/run/ssh-agent.pid 2>/dev/null || echo 0)
export SSH_AUTH_SOCK SSH_AGENT_PID

# Query the agent for loaded keys
ssh-add -l > "$STATUS_FILE" 2>&1
EC=$?

if [ $EC -ne 0 ]; then
    echo "Error: agent unreachable or no keys loaded (exit $EC)" >&2
    exit $EC
fi

echo "Verified: $(wc -l < "$STATUS_FILE") key(s) loaded in agent"
