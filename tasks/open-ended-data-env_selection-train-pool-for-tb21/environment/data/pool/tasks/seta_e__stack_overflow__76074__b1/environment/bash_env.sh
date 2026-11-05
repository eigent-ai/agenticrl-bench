#!/bin/bash
[ -n "$BASH_ENV_LOADED" ] && return
export BASH_ENV_LOADED=1

mkdir -p /var/run/appplatform

for plugin in metrics-collector legacy-auth-bridge deprecated-cache-sync event-logger rate-limiter; do
    exe="/opt/appplatform/bin/${plugin}.sh"
    pid_file="/var/run/appplatform/${plugin}.pid"
    manifest="/etc/appplatform/plugins/${plugin}.yaml"
    if [ -f "$exe" ] && [ -f "$manifest" ] && [ ! -f "$pid_file" ]; then
        bash "$exe" &
        echo $! > "$pid_file"
    fi
done
