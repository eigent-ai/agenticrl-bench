#!/bin/bash
set -e
DB="/opt/dbcatalog/catalog.db"
OUTDIR="/opt/dbcatalog/reports"
mkdir -p "$OUTDIR"
sqlite -header -csv "$DB" < /opt/dbcatalog/sql/all_tables.sql > "$OUTDIR/all_tables.csv"
sqlite -header -csv "$DB" < /opt/dbcatalog/sql/owner_tables.sql > "$OUTDIR/owner_tables.csv"
sqlite -header -csv "$DB" < /opt/dbcatalog/sql/table_columns.sql > "$OUTDIR/table_columns.csv"
echo "Reports generated successfully."
