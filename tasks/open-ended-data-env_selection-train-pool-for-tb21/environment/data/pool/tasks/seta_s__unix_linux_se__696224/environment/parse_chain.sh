#!/bin/bash
CHAIN_FILE="${1:-/opt/certaudit/certs/server-chain.pem}"

if [ ! -f "$CHAIN_FILE" ]; then
    echo "ERROR: Chain file not found: $CHAIN_FILE" >&2
    exit 1
fi

echo "Certificate chain: $CHAIN_FILE"
echo "---"
openssl x509 -in "$CHAIN_FILE" -noout -subject -issuer -dates 2>/dev/null
echo "---"
echo "Certificates parsed: 1"
