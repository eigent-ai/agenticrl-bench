#!/bin/bash
set -e

PKCS12_FILE="/opt/certs/bundle.pfx"
PASS_FILE="/opt/certs/.pfx_pass"
OUTPUT_DIR="/opt/certs/extracted"

mkdir -p "$OUTPUT_DIR"

PASS=$(cat "$PASS_FILE")

# Extract unencrypted private key
openssl pkcs12 -in "$PKCS12_FILE" \
    -nocerts -nodes \
    -passin "pass:$PASS" \
    -out "$OUTPUT_DIR/private.key"

# Extract client certificate
openssl pkcs12 -in "$PKCS12_FILE" \
    -clcerts -nokeys \
    -passin "pass:$PASS" \
    -out "$OUTPUT_DIR/client.crt"

# Extract CA certificate chain
openssl pkcs12 -in "$PKCS12_FILE" \
    -cacerts -nokeys \
    -passin "pass:$PASS" | openssl x509 -out "$OUTPUT_DIR/ca-chain.crt"

echo "Certificate extraction complete."
