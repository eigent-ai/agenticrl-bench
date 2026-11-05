#!/bin/bash
tmux new-session -d -s pipeline -x 200 -y 50
tmux send-keys -t pipeline "python3 /opt/scripts/generate_data.py" Enter
sleep 5
exec "$@"
