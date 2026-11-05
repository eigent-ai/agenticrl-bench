#!/bin/bash
BYTES=$(bash /opt/memtest/memavail.sh)
stress-ng --vm-bytes ${BYTES} -t 5s --metrics-brief 2>&1
