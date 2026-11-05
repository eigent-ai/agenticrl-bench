"""PhysicsBody node -- represents a physical entity in the game world."""

from __future__ import annotations
from typing import Tuple
from .node import Node


class PhysicsBody(Node):
    """A node with a physical presence (position, size, collision layer)."""

    def __init__(self, name: str = "PhysicsBody",
                 position: Tuple[float, float] = (0, 0),
                 size: Tuple[float, float] = (32, 32),
                 collision_layer: int = 1):
        super().__init__(name)
        self.position = position
        self.size = size
        self.collision_layer = collision_layer
        self.velocity = (0.0, 0.0)

    def move_to(self, x: float, y: float) -> None:
        self.position = (x, y)
