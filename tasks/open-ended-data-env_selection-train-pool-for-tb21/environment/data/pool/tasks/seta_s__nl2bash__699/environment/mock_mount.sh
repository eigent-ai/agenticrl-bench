#!/bin/bash
if [ $# -eq 0 ]; then
    cat /opt/diskmon/.mount_data
else
    /usr/bin/mount "$@"
fi
