#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

PID=$1
S=5

if [ ! -d "/proc/$PID" ]; then
    echo "Process $PID not found"
    exit 1
fi

rbytes=$(cat /proc/$PID/io 2>/dev/null | grep "^read_bytes" | awk '{print $2}')
wbytes=$(cat /proc/$PID/io 2>/dev/null | grep "^write_bytes" | awk '{print $2}')

sleep $S

rbytest=$(cat /proc/$PID/io 2>/dev/null | grep "^read_bytes" | awk '{print $2}')
wbytest=$(cat /proc/$PID/io 2>/dev/null | grep "^write_bytes" | awk '{print $2}')

echo "read_bytes: $((($rbytest-$rbytes)/1024/1024/$S)) MByte/s"
echo "write_bytes: $((($wbytest-$wbytest)/1024/1024/$S)) MByte/s"
