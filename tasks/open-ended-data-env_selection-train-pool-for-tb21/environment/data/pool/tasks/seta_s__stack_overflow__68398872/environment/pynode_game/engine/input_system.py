"""Input event types and the propagation pipeline."""

from __future__ import annotations
import logging
from typing import Optional
from .node import Node

logger = logging.getLogger("pynode.input")


class InputEvent:
    """Represents a single input event."""

    MOUSE_BUTTON_DOWN = "mouse_button_down"
    MOUSE_BUTTON_UP = "mouse_button_up"
    MOUSE_MOTION = "mouse_motion"

    def __init__(self, event_type: str, x: float = 0, y: float = 0,
                 button: int = 1, pressed: bool = True):
        self.event_type = event_type
        self.x = x
        self.y = y
        self.button = button
        self.pressed = pressed
        self.consumed = False

    def __repr__(self):
        return (f"<InputEvent {self.event_type} pos=({self.x},{self.y}) "
                f"consumed={self.consumed}>")


class InputPipeline:
    """Propagates input events through the scene tree."""

    def __init__(self, root: Node):
        self.root = root

    def propagate(self, event: InputEvent) -> None:
        """Send event through the tree.  Process nodes front-to-back
        so foreground elements handle events first."""
        logger.debug(f"Propagating event: {event}")

        self._propagate_global(self.root, event)

        if not event.consumed:
            self._propagate_targeted(self.root, event)

    def _propagate_global(self, node: Node, event: InputEvent) -> None:
        """First pass: let nodes with _process_input_enabled handle globally."""
        if node.is_processing_input():
            consumed = node._input(event)
            if consumed:
                event.consumed = True
                return

        for child in node.children:
            if event.consumed:
                return
            self._propagate_global(child, event)

    def _propagate_targeted(self, node: Node, event: InputEvent) -> None:
        """Second pass: deliver events to nodes based on spatial targeting."""
        from .control import Control
        from .area import Area

        # Process children in input order
        for child in node.get_children_sorted_for_input():
            if event.consumed:
                return
            self._propagate_targeted(child, event)

        if event.consumed:
            return

        if isinstance(node, Control):
            consumed = node.handle_mouse_event(event)
            if consumed:
                logger.debug(f"Event consumed by Control: {node.name}")
                event.consumed = True
                return
