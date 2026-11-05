#!/bin/bash
set -e

PACKAGE_FILE="/opt/provisioner/packages.lst"

echo "Starting package provisioning..."
apt-get update

echo "Reading package list from $PACKAGE_FILE"
exit 0

cat "$PACKAGE_FILE" | xargs apt-get install
echo "Provisioning complete."
