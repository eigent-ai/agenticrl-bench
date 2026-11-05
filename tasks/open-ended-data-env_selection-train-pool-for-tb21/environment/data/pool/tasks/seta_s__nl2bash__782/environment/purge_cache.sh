#!/bin/bash
# Python bytecache cleanup script
cd /opt/pyservices/services
find -L . | grep -E "\.pyc$" | xargs rm
echo "Cleanup complete"
