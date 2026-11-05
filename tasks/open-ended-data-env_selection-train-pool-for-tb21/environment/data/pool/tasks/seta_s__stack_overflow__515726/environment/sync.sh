#!/bin/bash
set -e

source /opt/filesync/filesync.conf

echo "Starting file sync..."
echo "Reading manifest from $MANIFEST_FILE"

cd "$OUTBOX_DIR"

for file in $(cat "$MANIFEST_FILE"); do
    local_name=$(echo "$file" | cut -d' ' -f1)
    remote_name=$(echo "$file" | cut -d' ' -f2)

    if [ -z "$local_name" ] || [ -z "$remote_name" ]; then
        continue
    fi

    echo "Transferring $local_name -> $remote_name"
    scp -P $SSH_PORT "$local_name" ${SSH_USER}@${SSH_HOST}:${INBOX_DIR}/${remote_name} || true

    mv "$local_name" done/ 2>/dev/null
done

echo "Sync complete."
