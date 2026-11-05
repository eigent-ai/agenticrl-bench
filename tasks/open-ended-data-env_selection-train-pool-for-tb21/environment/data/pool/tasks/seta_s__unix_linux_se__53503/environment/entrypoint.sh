#!/bin/bash
Xvfb :99 -screen 0 800x600x24 &
sleep 1
export DISPLAY=:99
exec "$@"
