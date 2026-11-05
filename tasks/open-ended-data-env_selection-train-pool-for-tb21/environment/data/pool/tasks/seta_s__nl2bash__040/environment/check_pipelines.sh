#!/bin/bash

API_URL="http://localhost:5000"
PROJECT_ID=1

pipelines=$(curl -s "${API_URL}/api/v3/projects/${PROJECT_ID}/pipelines")

failed=$(echo "$pipelines" | jq -r '.[] | select(.status == "failed") | .id')
if [ -n "$failed" ]; then
    echo "ALERT: Failed pipelines in project ${PROJECT_ID}: $failed"
fi

stuck=$(echo "$pipelines" | jq -r '.[] | select(.status == "pending") | .id')
if [ -n "$stuck" ]; then
    echo "ALERT: Stuck pipelines in project ${PROJECT_ID}: $stuck"
fi
