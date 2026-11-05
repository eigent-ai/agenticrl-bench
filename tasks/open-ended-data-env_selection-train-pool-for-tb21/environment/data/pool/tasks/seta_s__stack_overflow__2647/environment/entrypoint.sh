#!/bin/bash
service postgresql start
# Wait until PostgreSQL is ready to accept connections
for i in $(seq 1 30); do
    su -c "pg_isready -q" postgres && break
    sleep 1
done
exec "$@"
