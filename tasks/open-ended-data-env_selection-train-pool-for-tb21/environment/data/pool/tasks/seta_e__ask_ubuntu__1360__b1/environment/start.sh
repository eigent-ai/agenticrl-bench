#!/bin/bash
# Start Apache if not already running
if ! pgrep -x apache2 > /dev/null; then
    apachectl start
fi
exec "$@"
