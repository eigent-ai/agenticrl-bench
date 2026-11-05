#!/bin/bash
# Start background services then hand off to shell
/opt/procwatch/start_services.sh
exec "$@"
