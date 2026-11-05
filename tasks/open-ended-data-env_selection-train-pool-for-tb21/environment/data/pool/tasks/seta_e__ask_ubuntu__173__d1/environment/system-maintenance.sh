#!/bin/bash
echo "Running system maintenance..."
echo "Checking disk space..."
df -h / | grep -E "Filesystem|/$"
echo "Maintenance check complete"
