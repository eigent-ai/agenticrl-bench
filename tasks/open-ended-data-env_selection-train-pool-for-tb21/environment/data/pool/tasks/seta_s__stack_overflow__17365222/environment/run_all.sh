#!/bin/bash
cd /opt/datamigration

echo "Running clean_paths.sql..."
sqlite3 warehouse.db < scripts/clean_paths.sql

echo "Running clean_articles.sql..."
sqlite3 warehouse.db < scripts/clean_articles.sql

echo "Running clean_codes.sql..."
sqlite3 warehouse.db < scripts/clean_codes.sql

echo "Running clean_locations.sql..."
sqlite3 warehouse.db < scripts/clean_locations.sql

echo "All cleanup scripts completed."
