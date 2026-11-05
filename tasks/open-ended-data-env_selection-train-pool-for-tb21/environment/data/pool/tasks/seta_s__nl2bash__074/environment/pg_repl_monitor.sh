#!/bin/bash

# PostgreSQL Replication Lag Monitor
THRESHOLD=30  # seconds

REPLICA_LAG=$(psql -p 5432 -U postgres -t -c \
  "SELECT EXTRACT(EPOCH FROM now() - pg_last_xact_replay_timestamp())/60" \
  2>/dev/null | tail -3 | head -1 | cut -d' ' -f3)

if [ "$REPLICA_LAG" -gt "$THRESHOLD" ]; then
    echo "ALERT: Replication lag is ${REPLICA_LAG} seconds" | \
      mail -s "PostgreSQL Replication Alert" root
fi
