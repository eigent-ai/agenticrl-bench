import signal
import sys
import traceback

from debuglib.config import LOG_PATH


def _signal_handler(signum, frame):
    """Dump the current call stack for debugging purposes."""
    traceback.print_stack(file=sys.stderr)


def install_signal_handler():
    """Install a signal handler that dumps the stack trace to the debug log."""
    signal.signal(signal.SIGUSR2, _signal_handler)
