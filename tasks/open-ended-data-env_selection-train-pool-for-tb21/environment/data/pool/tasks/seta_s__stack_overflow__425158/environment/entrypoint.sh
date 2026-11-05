#!/bin/bash
# Start MySQL and wait until it is ready
service mysql start

for i in $(seq 1 30); do
    if mysqladmin ping --silent 2>/dev/null; then
        break
    fi
    sleep 1
done

exec "$@"
