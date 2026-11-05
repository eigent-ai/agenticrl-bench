#!/bin/bash
SOURCE="/srv/webapp"
DEST="/backup/webapp"
ARCHIVE="/backup/webapp.tar.gz"
rm -rf "$DEST" "$ARCHIVE"
tar czf "$ARCHIVE" -C /srv webapp
tar xzf "$ARCHIVE" -C /backup --no-same-owner --no-same-permissions
