#!/bin/bash
set -e
TIMESTAMP=$(date +%Y%m%dT%H%M%S)
echo "${TIMESTAMP} restart triggered" > /var/webapp/restart.log
echo "Webapp restarted at ${TIMESTAMP}"
