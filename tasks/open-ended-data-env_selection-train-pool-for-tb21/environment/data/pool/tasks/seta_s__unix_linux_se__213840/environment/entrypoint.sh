#!/bin/bash
Xvfb :99 -screen 0 1024x768x24 &>/dev/null &
sleep 0.5
exec "$@"
