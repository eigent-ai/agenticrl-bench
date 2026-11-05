#!/bin/bash
# Minimal core-dump capture helper (replaces apport when kernel pipes cores here)
# Called by the kernel as: apport -p<pid> -s<signal> -c<rlimit> ...
# The core dump content is piped to stdin.

PID=""
for arg in "$@"; do
    case "$arg" in
        -p*) PID="${arg#-p}" ;;
    esac
done

if [ -n "$PID" ]; then
    DEST="/tmp/core.${PID}"
else
    DEST="/tmp/core"
fi

# Write the core from stdin to disk
cat > "$DEST"

# Also copy to /tmp/core for easy discovery
[ "$DEST" != "/tmp/core" ] && cp "$DEST" "/tmp/core" 2>/dev/null || true
