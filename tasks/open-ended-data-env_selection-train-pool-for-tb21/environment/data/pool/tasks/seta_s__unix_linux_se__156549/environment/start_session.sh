#!/bin/bash
source /opt/xci/setup_display.sh
openbox >/tmp/wm.log 2>&1 &
echo $! > /tmp/ci-wm.pid
sleep 1
xclock >/tmp/xclock.log 2>&1 &
echo $! > /tmp/ci-xclock.pid
sleep 1
