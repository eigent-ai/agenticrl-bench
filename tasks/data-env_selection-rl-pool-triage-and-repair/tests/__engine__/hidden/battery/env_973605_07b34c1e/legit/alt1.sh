#!/bin/bash
set -euo pipefail
src=/home/developer/webapp
declare -A links=(
    [/var/deploy/web]=$src/frontend
    [/var/deploy/api]=$src/backend
    [/var/deploy/common]=$src/shared
    [/etc/webapp/environment]=$src/config/.env
    [/etc/webapp/secrets]=$src/config/.secrets
)
install -d -m 0755 /var/deploy /etc/webapp
stamp=$(date +%Y%m%d%H%M%S)
for link in "${!links[@]}"; do
    target=${links[$link]}
    [ -e "$target" ] || { echo "missing target $target" >&2; exit 1; }
    if [ -L "$link" ]; then
        rm -f "$link"
    elif [ -e "$link" ]; then
        mkdir -p /var/backups/deploy-stale
        mv "$link" "/var/backups/deploy-stale/$(basename "$link").$stamp"
    fi
    ln -s "$target" "$link"
done
for link in "${!links[@]}"; do
    [ "$(readlink "$link")" = "${links[$link]}" ] && [ -e "$link" ]
done
