#!/bin/bash
source /opt/ci_gl/config.env

# Start X virtual framebuffer for headless rendering
Xvfb :0 -screen 0 ${SCREEN_RES}x${SCREEN_DEPTH} >/tmp/xvfb.log 2>&1 &
XVFB_PID=$!
echo $XVFB_PID > /tmp/xvfb.pid
sleep 1
echo "Display server started (PID: $XVFB_PID)"
