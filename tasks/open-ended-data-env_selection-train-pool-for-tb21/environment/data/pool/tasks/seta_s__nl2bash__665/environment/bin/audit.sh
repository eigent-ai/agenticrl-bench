#!/bin/bash
# Appends a log entry for a provisioned workspace
# Usage: audit.sh <token> <job_id> <owner>

TOKEN="$1"
JOB_ID="$2"
OWNER="$3"
TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S")

echo "$TIMESTAMP | token=$TOKEN | job=$JOB_ID | owner=$OWNER | status=provisioned" >> /opt/workspace-manager/logs/audit.log
