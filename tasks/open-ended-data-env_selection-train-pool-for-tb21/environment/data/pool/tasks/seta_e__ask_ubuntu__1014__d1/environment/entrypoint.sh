#!/bin/bash

# Entrypoint script that initializes dbus for the container

# Start dbus daemon if not already running
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    eval $(dbus-launch --sh-syntax)
    export DBUS_SESSION_BUS_ADDRESS
fi

# Execute the original command or start a shell
exec "$@"
