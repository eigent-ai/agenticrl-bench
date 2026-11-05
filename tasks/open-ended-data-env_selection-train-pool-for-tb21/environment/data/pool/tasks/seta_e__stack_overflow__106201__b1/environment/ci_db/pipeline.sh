#!/bin/bash
set -e

echo "[1/3] Starting database server..."
bash /opt/ci_db/start_postgres.sh

echo "[2/3] Setting up database environment..."
source /opt/ci_db/db_env.sh

echo "[3/3] Generating DB capability report..."
python3 /opt/ci_db/generate_report.py

echo "Pipeline completed. Report written to /tmp/db_report.json"
