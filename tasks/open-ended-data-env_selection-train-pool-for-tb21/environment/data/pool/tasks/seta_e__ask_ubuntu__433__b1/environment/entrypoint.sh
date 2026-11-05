#!/bin/bash
# Start PostgreSQL and then exec the command
su - postgres -c "/usr/lib/postgresql/16/bin/pg_ctl start -D /var/lib/postgresql/16/main -l /var/log/postgresql/postgresql.log -o '-c config_file=/etc/postgresql/16/main/postgresql.conf'" 2>/dev/null
# Wait for PostgreSQL to be ready
for i in $(seq 1 30); do
    if su - postgres -c "pg_isready" >/dev/null 2>&1; then
        break
    fi
    sleep 1
done
exec "$@"
