import time


class QueryLog:
    """Records executed queries for debugging and profiling."""

    def __init__(self):
        self._enabled = False
        self._log = []

    def enable(self):
        """Enable query logging."""
        self._enabled = True
        self._log = []

    def disable(self):
        """Disable query logging."""
        self._enabled = False

    def is_enabled(self):
        """Check if logging is enabled."""
        return self._enabled

    def log_query(self, query, bindings, elapsed=0.0):
        """Log an executed query with its bindings and execution time."""
        if not self._enabled:
            return
        self._log.append({
            "query": query,
            "time": elapsed,
        })

    def get_log(self):
        """Return all logged queries."""
        return list(self._log)

    def clear(self):
        """Clear the query log."""
        self._log = []
