#!/bin/bash
# ./run.sh start [--pidfile]
cd "$(dirname "$0")"
case "$1" in
  start)
    nohup python3 stockd.py > /tmp/stockd.log 2>&1 &
    [ "$2" = "--pidfile" ] && echo $! > /srv/stock/stockd.pid
    echo "stockd starting"
    ;;
  *) echo "usage: $0 start [--pidfile]"; exit 2 ;;
esac
