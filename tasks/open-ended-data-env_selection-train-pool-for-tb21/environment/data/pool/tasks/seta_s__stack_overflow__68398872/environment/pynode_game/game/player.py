"""Player character as a PhysicsBody node."""

from __future__ import annotations
import logging
from engine.physics_body import PhysicsBody

logger = logging.getLogger("pynode.game.player")


class Player(PhysicsBody):
    def __init__(self, position=(0, 0)):
        super().__init__("Player", position, size=(24, 48), collision_layer=1)
        self.checkpoints_reached = []
        self.flags_triggered = []

    def on_checkpoint(self, zone):
        """Called when the player enters a checkpoint trigger zone."""
        self.checkpoints_reached.append(zone.name)
        logger.info(f"Player reached checkpoint: {zone.name}")

    def on_flag(self, zone):
        """Called when the player enters a flag trigger zone."""
        self.flags_triggered.append(zone.name)
        logger.info(f"Player triggered flag: {zone.name}")
