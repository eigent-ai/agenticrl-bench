#!/bin/bash
set -e
ARTIFACT="${1:?Usage: verify_artifact.sh <artifact>}"
SIG="${ARTIFACT}.asc"
TRUSTED_KEYRING="/opt/release/trusted-keyring.gpg"

STATUS=$(gpg --no-default-keyring \
             --keyring "${TRUSTED_KEYRING}" \
             --batch --status-fd 1 \
             --verify "${SIG}" "${ARTIFACT}" 2>/dev/null)

if echo "$STATUS" | grep -q '^\[GNUPG:\] GOODSIG' && \
   ! echo "$STATUS" | grep -q '^\[GNUPG:\] KEYEXPIRED'; then
    echo "Signature verified successfully."
else
    echo "Signature verification failed (expired key or invalid signature)." >&2
    exit 1
fi
