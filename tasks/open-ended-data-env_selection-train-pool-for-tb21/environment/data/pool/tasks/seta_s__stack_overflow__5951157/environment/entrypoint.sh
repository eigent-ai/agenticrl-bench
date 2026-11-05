#!/bin/bash
set -e

# Start MySQL
usermod -d /var/lib/mysql/ mysql 2>/dev/null || true
service mysql start

# Wait for MySQL to accept connections (initially passwordless root via auth_socket)
for i in $(seq 1 60); do
    if mysql -u root -e "SELECT 1" &>/dev/null; then
        break
    fi
    sleep 1
done

# Load init SQL to set the password and create the database
mysql -u root < /app/init.sql

# Keep container alive
exec tail -f /dev/null
