#!/bin/bash
set -e

# Start PostgreSQL temporarily to create CI user and database
pg_ctlcluster 16 main start --

# Wait for PostgreSQL to be ready
for i in $(seq 1 30); do
    if pg_isready -q 2>/dev/null; then
        break
    fi
    sleep 1
done

# Create the CI user and test database
su - postgres -c "psql -c \"CREATE ROLE ci_runner WITH LOGIN PASSWORD 'ci_pass';\""
su - postgres -c "psql -c \"CREATE DATABASE ci_test OWNER ci_runner;\""

# Stop PostgreSQL - the pipeline is responsible for starting it
pg_ctlcluster 16 main stop --
