#!/bin/bash
DOMAIN="$1"
INTERFACE="$2"
STATE="$3"

if [ -z "$DOMAIN" ] || [ -z "$INTERFACE" ] || [ -z "$STATE" ]; then
    echo "Usage: $0 <domain> <interface> <state>" >&2
    exit 1
fi

if [ "$STATE" != "up" ] && [ "$STATE" != "down" ]; then
    echo "ERROR: state must be 'up' or 'down'" >&2
    exit 1
fi

echo "Current link state of $INTERFACE on domain $DOMAIN:"
virsh domif-status "$DOMAIN" "$INTERFACE"

echo "Setting $INTERFACE to $STATE on domain $DOMAIN..."
virsh domif-setlink "$STATE" "$DOMAIN" "$INTERFACE"

echo "Link state updated."
