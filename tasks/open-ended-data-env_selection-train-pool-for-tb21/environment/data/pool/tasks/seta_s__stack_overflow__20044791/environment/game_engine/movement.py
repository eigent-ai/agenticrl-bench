import math


class MovementSystem:
    """Handles movement logic for game entities."""

    def chase_player(self, enemy, target):
        """Move enemy toward the target position."""
        enemy.x = target.x
        enemy.y = target.y
