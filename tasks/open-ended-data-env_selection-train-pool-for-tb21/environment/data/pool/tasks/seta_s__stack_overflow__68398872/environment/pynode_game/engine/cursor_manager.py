"""Cursor shape management for hover feedback."""

from __future__ import annotations
import logging

logger = logging.getLogger("pynode.cursor")


CURSOR_ARROW = "arrow"
CURSOR_POINTING_HAND = "pointing_hand"
CURSOR_GRAB = "grab"
CURSOR_GRABBING = "grabbing"


class CursorManager:
    """Manages the current cursor shape based on hover state."""

    def __init__(self):
        self.current_shape: str = CURSOR_ARROW
        self._area_cursor_map: dict = {}
        self._hovered_area = None

    def register_area(self, area, hover_cursor: str = CURSOR_POINTING_HAND) -> None:
        self._area_cursor_map[id(area)] = hover_cursor

    def on_mouse_entered_area(self, area) -> None:
        """Called when the mouse enters an interactive area."""
        self._hovered_area = area
        cursor = self._area_cursor_map.get(id(area), CURSOR_POINTING_HAND)
        self.current_shape = cursor
        logger.debug(f"Cursor changed to {cursor} over {area.name}")

    def on_mouse_exited_area(self, area) -> None:
        """Called when the mouse exits an interactive area."""
        if self._hovered_area is area:
            self._hovered_area = None
            self.current_shape = CURSOR_ARROW
            logger.debug(f"Cursor reverted to arrow from {area.name}")

    # Legacy camelCase aliases that some code incorrectly references
    def onMouseEnteredArea(self, area) -> None:
        self.on_mouse_entered_area(area)

    def onMouseExitedArea(self, area) -> None:
        self.on_mouse_exited_area(area)
