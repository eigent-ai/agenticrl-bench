#!/bin/bash
set -euo pipefail
echo "=== CMS Nightly Cleanup ==="
for script in /opt/cms/sql/01_*.sql /opt/cms/sql/02_*.sql /opt/cms/sql/03_*.sql /opt/cms/sql/04_*.sql; do
    echo "Running: $script"
    mysql -u root cms_prod < "$script"
    echo "Done: $script"
done
echo "=== Cleanup Complete ==="
