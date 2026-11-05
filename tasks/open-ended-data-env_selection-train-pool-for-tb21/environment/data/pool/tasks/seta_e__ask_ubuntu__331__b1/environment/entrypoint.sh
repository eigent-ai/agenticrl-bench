#!/bin/bash
service mysql start

# Wait for MySQL to be ready
for i in $(seq 1 30); do
    if mysqladmin ping -u root --silent 2>/dev/null; then
        break
    fi
    sleep 1
done

exec "$@"
