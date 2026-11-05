#!/bin/bash
# Repository Key Rotation Script
# Maintained by: infrastructure team
# Schedule: Monthly via cron (see /etc/cron.d/repo-keys)
#
# This script refreshes the repository signing key from the central keyserver.
# If the keyserver is unavailable, the existing key remains valid until expiry.

KEY_ID="repo@local"
KEYSERVER="hkps://keys.example.invalid"

echo "Refreshing repository signing key from ${KEYSERVER}..."
gpg --keyserver "${KEYSERVER}" --recv-keys "${KEY_ID}" 2>&1

if [ $? -eq 0 ]; then
    echo "Key refreshed successfully."
    gpg --armor --export "${KEY_ID}" > /opt/repo-management/keys/repo-signing-key.asc
    echo "Updated key exported to /opt/repo-management/keys/"
else
    echo "WARNING: Could not reach keyserver. Key rotation skipped."
    echo "Current key remains valid. Will retry on next scheduled run."
fi
