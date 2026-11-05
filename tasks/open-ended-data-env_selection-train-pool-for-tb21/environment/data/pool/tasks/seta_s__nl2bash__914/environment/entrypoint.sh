#!/bin/bash
if ! pgrep -f 'ingest_daemon' > /dev/null 2>&1; then
    /opt/pipeline/start_pipeline.sh
fi
exec "${@:-bash}"
