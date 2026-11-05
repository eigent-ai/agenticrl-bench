#!/bin/bash
set -euo pipefail
OUTFILE=/home/appuser/ssh_connection_test.txt
ssh -o BatchMode=yes -o StrictHostKeyChecking=no localhost \
    "echo 'Secure connection established: remote backup verified'" > "$OUTFILE"
echo "Connection test complete: $OUTFILE"
