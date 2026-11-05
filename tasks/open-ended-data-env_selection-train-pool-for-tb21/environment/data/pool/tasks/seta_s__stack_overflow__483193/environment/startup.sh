#!/bin/bash
# Start PostgreSQL and keep the container alive
pg_ctlcluster 16 main start
exec tail -f /dev/null
