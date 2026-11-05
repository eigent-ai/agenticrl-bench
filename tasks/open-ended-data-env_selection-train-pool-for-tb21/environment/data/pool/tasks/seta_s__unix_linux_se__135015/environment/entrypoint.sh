#!/bin/bash
cd /tmp && python3 -m http.server 80 &>/dev/null &
exec "$@"
