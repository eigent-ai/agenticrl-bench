#!/bin/bash
SESSIONS_FILE="$(dirname "$(realpath "$0")")/sessions.txt"

if [ ! -f "$SESSIONS_FILE" ]; then
    echo "No sessions file found"
    exit 0
fi

while IFS= read -r session; do
    [ -z "$session" ] && continue
    tmux kill-session "$session" 2>/dev/null || true
    echo "Killed session: $session"
done < "$SESSIONS_FILE"

rm -f "$SESSIONS_FILE"
echo "Cleanup complete"
