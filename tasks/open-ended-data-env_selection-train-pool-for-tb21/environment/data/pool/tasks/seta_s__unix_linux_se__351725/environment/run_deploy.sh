#!/bin/bash
LOG_FILE="/opt/deploy/logs/deploy.log"
mkdir -p "$(dirname "$LOG_FILE")"

bash /opt/deploy/agent_init.sh

ssh-add -l >> "$LOG_FILE" 2>&1
ssh -o StrictHostKeyChecking=no deployuser@localhost "echo DEPLOY_OK" >> "$LOG_FILE" 2>&1
