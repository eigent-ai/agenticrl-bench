#!/bin/bash
# Create development workspace with 4 panes

SESSION="dev"

# Kill existing session if present
tmux kill-session -t $SESSION 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION -x 200 -y 50

# Configure pane colors for this session
tmux set pane-border-fg magenta
tmux set pane-active-border-fg cyan

# Split into 4 panes
tmux split-window -h -t workspace
tmux split-window -v -t workspace:0.0
tmux split-window -v -t workspace:0.2

# Send commands to each pane
tmux send-keys -t workspace:0.0 'echo "editor"' C-m
tmux send-keys -t workspace:0.1 'echo "terminal"' C-m
tmux send-keys -t workspace:0.2 'echo "logs"' C-m
tmux send-keys -t workspace:0.3 'echo "tests"' C-m
