#!/bin/bash
set -e

# Start PostgreSQL
pg_ctlcluster 16 main start

# Wait for PostgreSQL to be ready
for i in $(seq 1 10); do
    if su - postgres -c "pg_isready" > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Create user and database
su - postgres -c "psql -c \"CREATE USER devuser WITH PASSWORD 'devpass';\""
su - postgres -c "psql -c \"CREATE DATABASE devdb OWNER devuser;\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE devdb TO devuser;\""

# Connect to devdb as postgres and grant schema permissions to devuser
su - postgres -c "psql -d devdb -c 'GRANT ALL ON SCHEMA public TO devuser;'"

# Run init SQL as devuser
PGPASSWORD=devpass psql -U devuser -d devdb -h localhost -f /tmp/init.sql

# Stop PostgreSQL
pg_ctlcluster 16 main stop
