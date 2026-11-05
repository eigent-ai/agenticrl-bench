#!/bin/bash
set -e
DBNAME="warehouse"
DBUSER="exporter"
OUTDIR="/opt/export/output"
mkdir -p "$OUTDIR"

# Export 1: Products
psql -U "$DBUSER" -d "$DBNAME" -c "COPY (SELECT * FROM products ORDER BY id) TO '$OUTDIR/products.csv' WITH CSV HEADER DELIMITER ',';"

# Export 2: Orders
psql -U "$DBUSER" -d "$DBNAME" -c "SELECT id, product_id, customer_id, quantity, order_date FROM orders ORDER BY id" -o "$OUTDIR/orders.csv" -F ','

# Export 3: Revenue Summary
psql -U "$DBUSER" -d "$DBNAME" -f /opt/export/queries/revenue_summary.sql

# Export 4: Customers
psql -U "$DBUSER" -d "$DBNAME" -f /opt/export/queries/customers.sql

# Export 5: Inventory
psql -U "$DBUSER" -d "$DBNAME" -c "\copy (SELECT * FROM inventory_view ORDER BY id) TO '$OUTDIR/inventory.csv' WITH CSV HEADER"
