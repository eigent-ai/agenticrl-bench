#!/bin/bash
# User password provisioning script
# Reads username:password pairs from the configuration file and applies
# SHA-512 password hashes to /etc/shadow for each active account.

CONF="/opt/provisioning/users.conf"

while IFS=: read -r username password; do
    [[ "$username" =~ ^# ]] && continue
    [[ -z "$username" ]] && continue

    # Only process accounts that are currently active
    account_status=$(passwd -S "$username" 2>/dev/null | awk '{print $2}')
    if [ "$account_status" != "P" ]; then
        echo "Skipping $username (account status: $account_status)"
        continue
    fi

    hash=$(mkpasswd -m sha-512 "$password")
    usermod -p "$hash" "$username"
    echo "Updated password for $username"
done < "$CONF"
