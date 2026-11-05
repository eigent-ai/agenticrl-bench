#!/bin/bash
set -e
source /root/.bashrc

INCOMING="/root/secure_backup/incoming"
OUTDIR="/root/secure_backup/encrypted"
RECIPIENT="backup-agent@server.local"

for f in "$INCOMING"/*.tar; do
    fname=$(basename "$f")
    echo "Encrypting $fname..."
    gpg --batch --yes --trust-model tofu+pgp \
        --recipient "$RECIPIENT" \
        --output "$OUTDIR/${fname}.gpg" \
        --encrypt "$f"
done
echo "All backups encrypted successfully."
