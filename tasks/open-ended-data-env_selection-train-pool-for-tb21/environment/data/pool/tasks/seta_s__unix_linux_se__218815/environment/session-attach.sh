#!/bin/bash
# Attach to a named tmux session, creating it if it does not exist.
# Usage: session-attach.sh [session-name]
SESSION="${1:-workspace}"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux attach-session -t "$SESSION"
else
    tmux new-session -d -s "$SESSION"
    echo "Created new session: $SESSION"
fi
