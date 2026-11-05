#!/bin/bash
set -e

# Start PostgreSQL cluster
pg_ctlcluster 16 main start

# Wait until PostgreSQL is accepting connections
for i in $(seq 1 30); do
    if sudo -u postgres psql -c "SELECT 1" > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Create the database and full schema
sudo -u postgres psql -f /tmp/schema.sql

# Set password for the postgres user (enables TCP password auth)
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"

# Allow password-based TCP connections from localhost
echo "host    all             all             127.0.0.1/32            md5" >> /etc/postgresql/16/main/pg_hba.conf

# Stop cleanly so the data directory is consistent
pg_ctlcluster 16 main stop
