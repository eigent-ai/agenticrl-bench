#!/bin/bash
set -e
cd /app
node date_report.js --locale th-TH
echo "Done. Report written to /app/report.json"
