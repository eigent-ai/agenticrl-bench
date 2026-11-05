#!/bin/bash
set -e

echo "Initializing database..."

# Generate pg_hba.conf from template
if [ -f /docker-entrypoint-initdb.d/pg_hba.conf.template ]; then
    envsubst < /docker-entrypoint-initdb.d/pg_hba.conf.template > /var/lib/postgresql/pg_hba.conf
    echo "pg_hba.conf generated from template"
fi

echo "Database initialization complete"
