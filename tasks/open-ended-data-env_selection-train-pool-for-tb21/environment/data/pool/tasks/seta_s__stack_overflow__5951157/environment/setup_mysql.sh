#!/bin/bash
# Start MySQL and initialize the database if not yet done.
# Idempotent — safe to call multiple times.

# Start MySQL if not already running
if ! pgrep -x mysqld > /dev/null; then
    service mysql start
    # Wait for socket auth to work
    until mysql -u root -e "SELECT 1" 2>/dev/null; do
        sleep 1
    done
fi

# Check if financial_db exists; if not, run init
if ! mysql -u root -psecret -e "USE financial_db" 2>/dev/null; then
    mysql -u root -e "SOURCE /app/init.sql"
fi
