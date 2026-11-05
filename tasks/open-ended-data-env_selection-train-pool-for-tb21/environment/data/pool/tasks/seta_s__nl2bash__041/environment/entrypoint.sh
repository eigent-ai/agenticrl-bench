#!/bin/bash

mkdir -p /opt/monitor /var/log /mnt/data /mnt/backup /mnt/scratch

exec "$@"
