#!/bin/bash
export DISPLAY=":1"
export XAUTHORITY="/tmp/.Xauthority-ci"
Xvfb :99 -screen 0 1280x1024x24 -ac >/tmp/xvfb.log 2>&1 &
echo $! > /tmp/ci-xvfb.pid
sleep 1
