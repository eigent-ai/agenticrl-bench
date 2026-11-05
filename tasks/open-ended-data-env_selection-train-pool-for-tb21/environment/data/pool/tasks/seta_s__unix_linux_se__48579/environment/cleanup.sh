#!/bin/bash
set -e
find /var/cache/myapp/tmp -name "*.tmp" -type f -delete
find /var/cache/myapp/sessions -name "*.sess" -type f -delete
find /var/cache/myapp/workspace -name "*.lock" -type f -delete
echo "Cleanup complete"
