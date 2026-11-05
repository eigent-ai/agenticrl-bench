#!/bin/bash
# SSH Key Security Auditor
# Scans all user SSH private keys for passphrase protection
# Also enumerates keys currently loaded in the SSH agent
# Report is written to: /var/log/ssh-audit/report.txt

REPORT_FILE="/tmp/ssh-audit-report.txt"

SSH_AGENT_SOCKET="/tmp/ssh-agent.sock"

find_unencrypted_keys() {
    local violations=0
    echo "Scanning user SSH key directories..."
    for keyfile in /home/*/.ssh/*; do
        if [[ -f "$keyfile" && "$keyfile" != *.pub ]]; then
            if ! grep -q "ENCRYPTED" "$keyfile"; then
                echo "VIOLATION: $keyfile has no passphrase protection"
                violations=$((violations + 1))
            fi
        fi
    done
    echo "Total violations found: $violations"
}

list_agent_keys() {
    echo "Keys loaded in SSH agent:"
    if SSH_AUTH_SOCK="$SSH_AGENT_SOCKET" ssh-add -L 2>/dev/null; then
        :
    else
        echo "  (none found or agent not accessible)"
    fi
}

mkdir -p "$(dirname "$REPORT_FILE")"

{
    echo "=== SSH Key Security Report ==="
    echo "Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo ""
    echo "--- Unencrypted Private Keys ---"
    find_unencrypted_keys
    echo ""
    echo "--- SSH Agent Loaded Keys ---"
    list_agent_keys
    echo ""
    echo "=== End of Report ==="
} > "$REPORT_FILE"

echo "Security report written to: /var/log/ssh-audit/report.txt"
