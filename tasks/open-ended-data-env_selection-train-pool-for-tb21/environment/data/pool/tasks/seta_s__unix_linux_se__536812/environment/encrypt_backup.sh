#!/bin/bash
export GNUPGHOME=/etc/gpg-backup

RECIPIENT="backup@company.internal"
SOURCE_DIR="/var/data/plaintext"
DEST_DIR="/var/data/encrypted"

mkdir -p "$DEST_DIR"

for f in "$SOURCE_DIR"/*; do
    if [ -f "$f" ]; then
        gpg --batch --yes \
            --recipient "$RECIPIENT" \
            --output "$DEST_DIR/$(basename "$f").gpg" \
            --encrypt "$f"
    fi
done
