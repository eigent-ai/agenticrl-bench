#!/bin/bash
/usr/local/bin/start_services.sh
# Wait for services to accumulate activity
sleep 20
exec "$@"
