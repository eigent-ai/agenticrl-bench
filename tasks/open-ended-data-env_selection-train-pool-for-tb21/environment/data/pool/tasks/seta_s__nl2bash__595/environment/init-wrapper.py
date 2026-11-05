#!/usr/bin/env python3
"""Container init process - manages process lifecycle."""
import os
import signal
import time


def reap_children(signum, frame):
    """Reap all zombie children."""
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
        except ChildProcessError:
            break


# Run the setup script first (synchronously)
pid = os.fork()
if pid == 0:
    os.execv('/bin/bash', ['bash', '/opt/build-farm/setup/init-processes.sh'])
    os._exit(1)

# Wait for setup to complete
while True:
    try:
        _, status = os.waitpid(pid, 0)
        break
    except InterruptedError:
        continue
    except ChildProcessError:
        break

# Now install SIGCHLD handler for zombie reaping during normal operation
signal.signal(signal.SIGCHLD, reap_children)

# Keep container alive
while True:
    time.sleep(3600)
