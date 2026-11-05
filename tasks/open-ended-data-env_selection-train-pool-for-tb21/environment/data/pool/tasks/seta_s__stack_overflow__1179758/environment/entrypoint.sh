#!/bin/bash
/usr/local/bin/start_postgres.sh
exec "$@"
