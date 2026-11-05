#!/bin/bash
set -e
cd /opt/codesign

openssl cms -verify \
  -in releases/app-v1.0.tar.gz.sig \
  -inform DER \
  -CAfile ca/ca.crt \
  -out /dev/null

echo "Signature verified OK"
