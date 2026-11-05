#!/bin/bash
set -e
PROGRAM="${1:?Usage: run.sh <program>}"

exec su -s /bin/bash coderunner -c "
  ulimit -f 1024
  ulimit -t 10
  # ulimit -u 50
  ulimit -v 524288000
  exec $PROGRAM
"
