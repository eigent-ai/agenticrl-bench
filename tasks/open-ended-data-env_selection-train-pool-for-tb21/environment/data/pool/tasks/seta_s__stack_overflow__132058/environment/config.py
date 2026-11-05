"""Configuration module with property-access tracing."""

import sys
import traceback


class _PropertyTracer:
    """Configuration object that traces property accesses."""

    def __init__(self):
        self._data = {
            'data_dir': '/opt/logprocessor/data',
            'output_dir': '/opt/logprocessor/output',
            'max_threads': 2,
            'log_level': 'INFO',
        }
        self._access_log = '/opt/logprocessor/access.log'

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        data = super().__getattribute__('_data')
        if name in data:
            self._log_access(name)
            return data[name]
        raise AttributeError("Config has no attribute '{}'".format(name))

    def _log_access(self, name):
        """Log the call stack when a config property is accessed."""
        tb = traceback.format_tb(sys.exc_info()[2])
        with open(self._access_log, 'a') as f:
            f.write("Access: {}\n".format(name))
            for line in tb:
                f.write(line)
            f.write("\n")


Config = _PropertyTracer
