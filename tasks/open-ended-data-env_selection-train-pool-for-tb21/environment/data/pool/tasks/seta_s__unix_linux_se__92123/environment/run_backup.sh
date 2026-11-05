#!/bin/bash
BACKUP_ROOT="/backup/snapshots"
CURRENT="${BACKUP_ROOT}/current"

rsync -avz \
    --delete \
    --link-dest=/backup/previous \
    -e "ssh -i /opt/backup/.ssh/id_backup -o StrictHostKeyChecking=no -o BatchMode=yes" \
    root@localhost:/srv/website/ \
    "${CURRENT}/"
