#!/bin/bash
# Outputs "inside" if running inside a tmux session, "outside" otherwise.

if [ "$TERM" = "screen" ]; then
    echo "inside"
else
    echo "outside"
fi
