#!/bin/bash
source /opt/privcheck/lib/privcheck.sh

user="${1:-$(whoami)}"

if is_in_admin_group "$user"; then
    echo "User '$user' has administrative privileges."
    exit 0
else
    echo "User '$user' does not have administrative privileges."
    exit 1
fi
