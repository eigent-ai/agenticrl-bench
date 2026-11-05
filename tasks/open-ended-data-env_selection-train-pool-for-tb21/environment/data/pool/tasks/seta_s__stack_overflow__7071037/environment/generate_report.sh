#!/bin/bash
set -e

CONF_FILE="/opt/reports/db.conf"

# Parse config
HOST=$(grep '^host=' "$CONF_FILE" | cut -d'=' -f2)
USER=$(grep '^user=' "$CONF_FILE" | cut -d'=' -f2)
PASS=$(grep '^password=' "$CONF_FILE" | cut -d'=' -f2)
DB=$(grep '^database=' "$CONF_FILE" | cut -d'=' -f2)

MYSQL_CMD="mysql -h $HOST -u $USER -p$PASS $DB"

echo "Generating employee pricing report..."
$MYSQL_CMD --batch -N < /opt/reports/sql/employee_pricing.sql > /opt/reports/output/employee_pricing.csv

echo "Generating department summary report..."
$MYSQL_CMD --batch -N < /opt/reports/sql/department_summary.sql > /opt/reports/output/department_summary.csv

echo "Generating nearby facilities report..."
$MYSQL_CMD --batch -N < /opt/reports/sql/nearby_facilities.sql > /opt/reports/output/nearby_facilities.csv

echo "All reports generated successfully."
