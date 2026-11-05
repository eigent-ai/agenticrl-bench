"""graph4j error types."""


class InvalidConfigError(Exception):
    """Raised when environment contains invalid graph configuration variables."""
    pass


class ConnectionError(Exception):
    """Raised when connection to graph database fails."""
    pass
