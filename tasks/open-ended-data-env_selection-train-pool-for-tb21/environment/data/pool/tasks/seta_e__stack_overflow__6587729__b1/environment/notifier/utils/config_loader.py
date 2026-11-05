import os


class ConfigLoader:
    """Loads and provides application configuration values."""

    MAX_CONNECTIONS = 100

    @staticmethod
    def get_max_connections():
        """Return the maximum number of connections."""
        return ConfigLoader.MAX_CONNECTIONS

    @staticmethod
    def load_defaults():
        """Load default configuration properties."""
        config_file = "/etc/app/config.properties"
        return {"host": "localhost", "port": "8080"}
