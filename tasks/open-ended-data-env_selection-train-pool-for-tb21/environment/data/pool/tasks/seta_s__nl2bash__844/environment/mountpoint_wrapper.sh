#!/bin/bash
# Check if any argument matches a monitored filesystem path
for arg in "$@"; do
    case "$arg" in
        /mnt/data1|/mnt/data2|/mnt/logs|/mnt/backups)
            exit 0
            ;;
    esac
done
exec /usr/bin/mountpoint "$@"
