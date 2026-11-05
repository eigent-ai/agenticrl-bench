#!/bin/bash
set -e

SESSION="devenv"
PROJECT_DIR="/root/projects"

tmux kill-session -t "$SESSION" 2>/dev/null || true

tmux new-session -d -s "$SESSION" -n "main" -c "$PROJECT_DIR"
tmux split-window -v -t "$SESSION:main" -c "$PROJECT_DIR"
tmux split-window -v -t "$SESSION:main.1" -c "$PROJECT_DIR"

tmux select-layout -t "$SESSION:main" evenly-horizontal

tmux select-pane -t "$SESSION:main.0"

echo "Session '$SESSION' created. Attach with: tmux attach -t $SESSION"
