#!/bin/bash
# Creates virtual serial port pairs for the test bench

source /etc/serialports/config.sh

# Override port directory for this bench instance
PORT_DIR=/tmp/serial

mkdir -p "$PORT_DIR"
pkill -f "socat.*serial/ttyV" 2>/dev/null || true
sleep 0.2

for i in $(seq 0 $((NUM_PORTS - 1))); do
    socat -d \
        PTY,link=${PORT_DIR}/ttyV${i},raw,echo=0 \
        PTY,link=${PORT_DIR}/ttyV${i}_peer,raw,echo=0 \
        2>/dev/null &
    timeout 3 bash -c "while [ ! -L '${PORT_DIR}/ttyV${i}' ]; do sleep 0.1; done" || true
done

echo "Virtual serial bench ready: ${NUM_PORTS} pairs in ${PORT_DIR}"
