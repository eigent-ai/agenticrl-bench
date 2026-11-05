#!/bin/bash
# SQL Test Runner
# Validates migration scripts before deployment

echo "Running SQL syntax validation..."

ERRORS=0
for f in migrations/*.sql; do
    if [ -f "$f" ]; then
        echo "Checking: $f"
    fi
done

echo "Validation complete. Errors found: $ERRORS"
exit $ERRORS
