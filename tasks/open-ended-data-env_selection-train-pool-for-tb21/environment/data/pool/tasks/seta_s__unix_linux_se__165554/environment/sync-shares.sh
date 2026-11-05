#!/bin/bash
SRCDIR="/srv/samba/project"
DSTDIR="/srv/samba/backups/archive"
cp -u $SRCDIR/* $DSTDIR/
echo "Sync completed at $(date)" >> /var/log/sync-shares.log
