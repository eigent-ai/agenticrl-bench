#!/bin/bash
# dconf helper: initializes dbus session for headless dconf usage
# Source this file before running dconf commands: source /usr/local/bin/dconf-helper.sh
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    eval $(dbus-launch --sh-syntax)
    export DBUS_SESSION_BUS_ADDRESS
fi
export DCONF_PROFILE=/etc/dconf/profile/user
echo "dbus session initialized: $DBUS_SESSION_BUS_ADDRESS"
