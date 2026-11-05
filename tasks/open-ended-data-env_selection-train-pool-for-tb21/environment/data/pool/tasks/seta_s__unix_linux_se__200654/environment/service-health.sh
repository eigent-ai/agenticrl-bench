#!/bin/bash
WEBAPP_STATUS=$(ps aux | grep [w]ebapp | grep -v grep | wc -l)
INIT_STATUS=$(ps aux | grep [i]nit.sh | grep -v grep | wc -l)

if [ "$WEBAPP_STATUS" -gt 0 ] && [ "$INIT_STATUS" -gt 0 ]; then
    echo "All services healthy"
    exit 0
else
    echo "Service check failed"
    exit 1
fi
