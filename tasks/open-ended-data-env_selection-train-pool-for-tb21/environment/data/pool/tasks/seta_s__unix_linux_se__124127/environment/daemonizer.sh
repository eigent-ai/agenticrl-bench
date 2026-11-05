#!/bin/bash
# Classic double-fork daemonization
(
    # First fork already happened (subshell)
    # Now do the second fork
    (
        while true; do sleep 5; done
    ) &
    # First child exits
    exit 0
) &
# Original exits immediately
wait
exit 0
