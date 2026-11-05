"""Debug utilities for the log processor application."""

import os
import signal
import sys
import traceback
import threading


def _dump_stacks(signum, frame):
    """Handle SIGUSR1 by dumping thread stack traces."""
    output_path = '/var/log/logprocessor/debug.log'
    with open(output_path, 'w') as f:
        f.write("=== Stack Dump (signal {}) ===\n".format(signum))
        f.write("\n--- Main Thread ---\n")
        traceback.print_stack(frame, file=f)


def install_signal_handler():
    """Install SIGUSR1 handler for debugging."""
    signal.signal(signal.SIGUSR1, _dump_stacks)
