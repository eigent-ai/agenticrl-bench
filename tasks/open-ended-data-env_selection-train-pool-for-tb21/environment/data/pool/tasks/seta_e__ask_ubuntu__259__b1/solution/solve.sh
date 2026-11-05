#!/bin/bash

# Ensure OpenRC runtime is initialized for the container environment
mkdir -p /run/openrc
touch /run/openrc/softlevel

# Remove nginx from the default runlevel to prevent auto-start on boot
rc-update del nginx default

# Verify the change: nginx should no longer appear in default runlevel
rc-update show default

echo "Done! nginx has been disabled from auto-start but remains manually startable."
