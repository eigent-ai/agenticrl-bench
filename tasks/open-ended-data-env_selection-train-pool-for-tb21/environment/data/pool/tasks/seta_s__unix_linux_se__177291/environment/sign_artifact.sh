#!/bin/bash
set -e
source /opt/release/signing.conf
ARTIFACT="${1:?Usage: sign_artifact.sh <artifact>}"
gpg --batch --yes --detach-sign --armor -u "$SIGNING_KEY_FINGERPRINT" "$ARTIFACT"
echo "Signed: ${ARTIFACT}.asc"
