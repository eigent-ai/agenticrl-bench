#!/bin/bash
set -e

JOB_NAME=$1
if [ -z "$JOB_NAME" ]; then
    echo "Usage: $0 <job-name> <command...>" >&2
    exit 1
fi
shift
COMMAND="$*"

SESSION_NAME="job-${JOB_NAME}"
SESSIONS_FILE="$(dirname "$(realpath "$0")")/sessions.txt"

tmux new-session -s "$SESSION_NAME" "$COMMAND"

echo "$SESSION_NAME" >> "$SESSIONS_FILE"
echo "Started job in session: $SESSION_NAME"
