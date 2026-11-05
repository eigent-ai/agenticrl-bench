#!/bin/bash
mkdir -p /etc/ci
printf "last_update=%s\n" "$(date -Iseconds)" > /etc/ci/app.conf
