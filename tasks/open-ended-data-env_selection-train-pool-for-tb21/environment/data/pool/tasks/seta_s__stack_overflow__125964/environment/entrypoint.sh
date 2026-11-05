#!/bin/bash

mkdir -p /run/systemctl-state /var/log/journal-docker

for link in /etc/systemd/system/multi-user.target.wants/*.service; do
    if [ -L "$link" ]; then
        service_name=$(basename "$link")
        /usr/bin/systemctl start "$service_name" 2>&1 || true
    fi
done

exec "$@"
