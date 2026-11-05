#!/bin/bash
# Initialize dbus session for gsettings usage
mkdir -p /run/dbus
if [ ! -f /run/dbus/pid ]; then
    dbus-daemon --system --fork 2>/dev/null || true
fi
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    eval $(dbus-launch)
    export DBUS_SESSION_BUS_ADDRESS
fi
# Start dconf-service for settings persistence
if [ -f /usr/lib/dconf/dconf-service ]; then
    /usr/lib/dconf/dconf-service &
    sleep 1
fi
