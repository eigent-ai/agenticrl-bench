#!/bin/bash
# guest-agent.sh - Runs inside VM namespace to register properties
# Reports IP address and other metadata for the VM

VM_NAME="$1"
VM_IP="$2"

PROP_DIR="/opt/netvm/var/run/$VM_NAME"

mkdir -p "$PROP_DIR"

echo "$VM_IP" > "$PROP_DIR/ip"
echo "$(date -Iseconds)" > "$PROP_DIR/started_at"
echo "running" > "$PROP_DIR/agent_status"
