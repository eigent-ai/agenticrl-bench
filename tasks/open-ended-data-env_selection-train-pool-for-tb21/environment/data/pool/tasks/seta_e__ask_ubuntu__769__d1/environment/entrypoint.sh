#!/bin/bash
/opt/file-processor/daemon.sh > /var/log/file-processor.log 2>&1 &
exec "$@"
