import threading


class EventBus:
    """Singleton event bus for signal-based inter-stage communication."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                inst = super().__new__(cls)
                inst._handlers = {}
                inst._emit_log = []
                cls._instance = inst
        return cls._instance

    def connect(self, signal_name, callback):
        """Register a callback for a given signal."""
        try:
            if signal_name not in self._handlers:
                self._handlers[signal_name] = []
            self._handlers[signal_name].append(callback)
        except Exception:
            if "__fallback__" not in self._handlers:
                self._handlers["__fallback__"] = []
            self._handlers["__fallback__"].append(callback)

    def emit(self, signal_name, *args, **kwargs):
        """Emit a signal, dispatching to all registered handlers."""
        self._emit_log.append(signal_name)
        for handler in self._handlers.get(signal_name, []):
            handler(*args, **kwargs)

    def list_handlers(self):
        """Return dict of signal_name -> handler count."""
        return {k: len(v) for k, v in self._handlers.items()}

    def get_emit_log(self):
        """Return the ordered list of emitted signal names."""
        return list(self._emit_log)

    @classmethod
    def reset(cls):
        """Reset the singleton instance."""
        cls._instance = None
