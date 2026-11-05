"""Event bus for decoupled inter-system communication.

Entities and systems publish / subscribe to named events.  The bus
keeps a list of callbacks per event name and dispatches calls when
an event is emitted.
"""


class EventBus:
    """Simple publish-subscribe event dispatcher."""

    def __init__(self):
        self._listeners = {}

    def connect(self, event_name, callback):
        """Register *callback* to be called when *event_name* fires."""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        if callback not in self._listeners[event_name]:
            self._listeners[event_name].append(callback)

    def disconnect(self, event_name, callback):
        """Remove *callback* from *event_name* listeners."""
        if event_name not in self._listeners:
            return
        self._listeners[event_name] = [
            cb for cb in self._listeners[event_name] if cb is not callback
        ]

    def emit(self, event_name, *args, **kwargs):
        """Invoke all registered callbacks for *event_name*."""
        if event_name not in self._listeners:
            return
        for callback in list(self._listeners[event_name]):
            try:
                callback(*args, **kwargs)
            except Exception as exc:
                import logging
                logging.getLogger("events").warning(
                    "Callback %s for event '%s' raised: %s",
                    callback, event_name, exc,
                )

    def clear(self, event_name=None):
        if event_name:
            self._listeners.pop(event_name, None)
        else:
            self._listeners.clear()

    def listener_count(self, event_name):
        return len(self._listeners.get(event_name, []))
