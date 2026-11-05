#!/bin/bash
posix=0
for arg in "$@"; do
    case "$arg" in
        -P) posix=1 ;;
    esac
done

if [ $posix -eq 1 ]; then
    cat /opt/diskmon/.df_data_posix
else
    cat /opt/diskmon/.df_data
fi
