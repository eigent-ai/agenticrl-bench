#!/bin/bash
# start-desktop.sh - Launch X11 desktop session inside the container
# Starts Xorg on a dedicated VT with a window manager

set -euo pipefail

DISPLAY_NUM=":10"
VT="vt07"
WM="${WM:-openbox}"

export HOME="${HOME:-/root}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/0}"

# Ensure we're on the correct virtual terminal
if [ "$XDG_VTNR" = "10" ]; then
    echo "Already on VT10, proceeding with X startup"
else
    echo "Warning: Not on expected VT (XDG_VTNR=$XDG_VTNR)"
fi

# Create runtime directory
mkdir -p "$XDG_RUNTIME_DIR"
chmod 0700 "$XDG_RUNTIME_DIR"

# Prepare Xorg configuration
XORG_CONF_DIR="/opt/lxc-desktop/xorg.conf.d"

echo "Starting X server on display ${DISPLAY_NUM} (${VT})"

# Launch X server
/usr/bin/Xorg "${DISPLAY_NUM}" "${VT}" \
    -configdir "${XORG_CONF_DIR}" \
    -logfile "/var/log/Xorg.${DISPLAY_NUM}.log" \
    -noreset \
    -keeptty &

XPID=$!
sleep 2

# Set display for clients
export DISPLAY="${DISPLAY_NUM}"

# Start window manager
echo "Starting window manager: ${WM}"
${WM} &

# Start session services
if command -v dbus-launch &>/dev/null; then
    eval $(dbus-launch --sh-syntax)
fi

echo "Desktop session started (PID: ${XPID})"
wait ${XPID}
