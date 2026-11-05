#!/bin/bash
source /opt/ci_db/config.env

# Configure and start PostgreSQL for CI testing
sed -i "s/^#\?port = .*/port = 5432/" /etc/postgresql/16/main/postgresql.conf
pg_ctlcluster 16 main start --
sleep 2
echo "PostgreSQL started on port 5432"
