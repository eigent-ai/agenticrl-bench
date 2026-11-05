"""Trigger zones for flags and checkpoints."""

from __future__ import annotations
import logging
from engine.area import Area

logger = logging.getLogger("pynode.game.triggers")


class FlagZone(Area):
    def __init__(self, name: str = "FlagZone", position=(0, 0),
                 size=(60, 60)):
        super().__init__(name, position, size,
                         interaction_layer=4, interaction_mask=1)
        self.activated = False
        self.z_index = 1

    def on_body_entered(self, body, shape_index: int = 0):
        self.activated = True
        logger.info(f"{self.name} activated by {body.name}")


class CheckpointZone(Area):
    def __init__(self, name: str = "CheckpointZone", position=(0, 0),
                 size=(60, 60)):
        super().__init__(name, position, size,
                         interaction_layer=4, interaction_mask=1)
        self.saved = False
        self.z_index = 1

    def on_body_entered(self, body, shape_index: int = 0):
        self.saved = True
        logger.info(f"{self.name} saved by {body.name}")
