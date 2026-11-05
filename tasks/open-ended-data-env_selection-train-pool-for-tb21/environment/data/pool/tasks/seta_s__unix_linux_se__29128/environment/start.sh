#!/bin/bash
DB_HOST=db.internal
DB_PORT=5432
DB_USER=admin
export DB_PASS=s3cr3t_pass

python3 /opt/webapp/server.py &
echo $! > /var/run/webapp.pid
