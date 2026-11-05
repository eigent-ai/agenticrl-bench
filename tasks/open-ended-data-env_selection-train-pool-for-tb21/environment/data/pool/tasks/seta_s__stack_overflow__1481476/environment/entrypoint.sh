#!/bin/bash
pg_ctlcluster 16 main start 2>/dev/null || service postgresql start 2>/dev/null || true
sleep 1
exec "$@"
