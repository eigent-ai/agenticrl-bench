"""HUD overlay for the puzzle game."""

from __future__ import annotations
import logging
from engine.control import Control

logger = logging.getLogger("pynode.game.hud")


class HUD(Control):
    """Full-screen HUD overlay that displays game info.

    The HUD covers the entire screen.  Its background panels are
    transparent and should not intercept mouse events meant for the
    game world beneath.
    """

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        super().__init__("HUD", position=(0, 0),
                         size=(screen_width, screen_height))
        self.z_index = 100
        self.interaction_count = 0
        self.status_text = "No interactions detected"

    def record_interaction(self):
        self.interaction_count += 1
        self.status_text = f"Interactions: {self.interaction_count}"
