#!/bin/bash
# Enrollment Migration Pipeline
# Consolidates student data from department databases into unified.db

sqlite3 /opt/enrollment/unified.db < /opt/enrollment/schema.sql

for f in /opt/enrollment/sql/*.sql; do
    echo "Running $f ..."
    sqlite3 /opt/enrollment/unified.db < "$f"
done

echo "Migration complete."
