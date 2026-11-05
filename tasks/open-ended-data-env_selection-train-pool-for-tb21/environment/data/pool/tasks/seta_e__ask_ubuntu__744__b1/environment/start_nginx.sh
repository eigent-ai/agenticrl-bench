#!/bin/bash
# Start nginx if not already running
if ! pgrep -x nginx > /dev/null 2>&1; then
    nginx 2>/dev/null || true
fi
