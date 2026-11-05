#!/bin/bash
SESSIONS_FILE="$(dirname "$(realpath "$0")")/sessions.txt"

if [ ! -f "$SESSIONS_FILE" ]; then
    echo "No sessions file found"
    exit 0
fi

echo "Active job sessions:"
while IFS= read -r session; do
    [ -z "$session" ] && continue
    if tmux ls 2>/dev/null | grep -q "^${session}$"; then
        echo "  RUNNING: $session"
    else
        echo "  STOPPED: $session"
    fi
done < "$SESSIONS_FILE"
