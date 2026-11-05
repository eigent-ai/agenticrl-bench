#!/bin/bash
# passcheck.sh - Verify a password against the stored SHA-256 hash
#
# Usage:
#   Interactive : ./passcheck.sh
#   Scripted    : printf '%s' "password" | ./passcheck.sh
#
# Exit codes: 0=correct password, 1=wrong password, 2=configuration error

set -e

HASH_FILE="/opt/passcheck/passhash"
PROMPT="Password: "

if [ ! -f "$HASH_FILE" ]; then
    printf "Error: password not configured. Run setup.sh first.\n" >&2
    exit 2
fi

stored_hash=$(cat "$HASH_FILE")

stty -echo
printf "%s" "$PROMPT" >&2
read -r password
stty echo
printf "\n" >&2

input_hash=$(echo "$password" | sha256sum | cut -d' ' -f1)

if [ "$input_hash" = "$stored_hash" ]; then
    exit 0
else
    exit 1
fi
