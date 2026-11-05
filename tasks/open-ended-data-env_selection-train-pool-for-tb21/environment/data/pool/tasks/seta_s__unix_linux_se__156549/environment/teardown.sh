#!/bin/bash
for pidfile in /tmp/ci-xclock.pid /tmp/ci-wm.pid /tmp/ci-xvfb.pid; do
    if [ -f "$pidfile" ]; then
        kill "$(cat "$pidfile")" 2>/dev/null || true
        rm -f "$pidfile"
    fi
done
