#!/bin/bash
losetup -f /opt/images/data.img
losetup -f /opt/images/backup.img
exec "$@"
