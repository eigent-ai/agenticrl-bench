#!/bin/bash
mkdir -p /tmp/webshot
Xvfb :9 -screen 0 1280x1024x24 > /tmp/webshot/xvfb.log 2>&1 &
XVFB_PID=$!
echo $XVFB_PID > /tmp/webshot/xvfb.pid
sleep 2
echo "Virtual display started (PID: $XVFB_PID)"
