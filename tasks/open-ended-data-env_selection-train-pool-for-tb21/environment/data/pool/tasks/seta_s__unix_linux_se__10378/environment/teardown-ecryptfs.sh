#!/bin/bash
# PAM session teardown for ecryptfs-style private directories
[ "$PAM_TYPE" = "close_session" ] || exit 0

USER_HOME=$(getent passwd "$PAM_USER" | cut -d: -f6)
ECRYPTFS_DIR="$USER_HOME/.ecryptfs"

if [ -f "$ECRYPTFS_DIR/auto-umount" ]; then
    MNT_POINT=$(cat "$ECRYPTFS_DIR/Private.mnt" 2>/dev/null)
    if [ -n "$MNT_POINT" ] && [ -f "$MNT_POINT/.vault-active" ]; then
        rm -rf "$MNT_POINT"/*
        rm -f "$MNT_POINT/.vault-active"
        logger -t pam_ecryptfs "Unmounted $MNT_POINT for $PAM_USER"
    fi
fi
