#!/bin/bash
Xvfb :0 -screen 0 1280x1024x24 &
sleep 2
exec "$@"
