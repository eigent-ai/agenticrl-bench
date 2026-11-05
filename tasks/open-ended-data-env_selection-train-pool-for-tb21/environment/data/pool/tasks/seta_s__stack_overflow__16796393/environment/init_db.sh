#!/bin/bash
# Initialize MySQL and set up the logmon database
service mysql start

# Wait for MySQL to be ready
for i in $(seq 1 30); do
    if mysqladmin ping --silent 2>/dev/null; then
        break
    fi
    sleep 1
done

# Run the schema setup
mysql < /opt/logmon/db_setup.sql

echo "Database initialized."
