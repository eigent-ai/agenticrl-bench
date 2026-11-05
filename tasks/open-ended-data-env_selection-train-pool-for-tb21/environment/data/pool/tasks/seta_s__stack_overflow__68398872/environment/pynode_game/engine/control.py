"""Control node -- UI element that can intercept mouse events."""

from __future__ import annotations
from typing import Tuple
from .node import Node


MOUSE_FILTER_STOP = "stop"
MOUSE_FILTER_PASS = "pass"
MOUSE_FILTER_IGNORE = "ignore"


class Control(Node):
    """A UI control node. Can intercept mouse events via mouse_filter.

    mouse_filter modes:
      - "stop":   consume the event (default, prevents propagation)
      - "pass":   handle event but let it continue propagating
      - "ignore": completely transparent to mouse events
    """

    def __init__(self, name: str = "Control",
                 position: Tuple[float, float] = (0, 0),
                 size: Tuple[float, float] = (100, 100),
                 mouse_filter: str = MOUSE_FILTER_STOP):
        super().__init__(name)
        self.position = position
        self.size = size
        self.mouse_filter = mouse_filter

    def contains_point(self, x: float, y: float) -> bool:
        px, py = self.position
        sx, sy = self.size
        return px <= x <= px + sx and py <= y <= py + sy

    def handle_mouse_event(self, event) -> bool:
        """Process a mouse event according to mouse_filter.

        Returns True if the event was consumed (should not propagate).
        """
        if self.mouse_filter == MOUSE_FILTER_IGNORE:
            return False
        if not self.contains_point(event.x, event.y):
            return False
        if self.mouse_filter == MOUSE_FILTER_STOP:
            return True
        return False
