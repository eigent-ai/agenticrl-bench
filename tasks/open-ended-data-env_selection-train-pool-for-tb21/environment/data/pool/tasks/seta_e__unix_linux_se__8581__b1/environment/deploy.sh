#!/bin/bash
set -e
TIMESTAMP=$(date +%Y%m%dT%H%M%S)
echo "${TIMESTAMP} deploy triggered" > /var/webapp/deploy.log
echo "Webapp deployed at ${TIMESTAMP}"
