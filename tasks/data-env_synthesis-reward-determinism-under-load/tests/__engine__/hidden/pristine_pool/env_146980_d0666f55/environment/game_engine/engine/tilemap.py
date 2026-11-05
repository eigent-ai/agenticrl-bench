"""Background tilemap renderer.

Renders a procedural grid of colored tiles to represent the game world floor.
Tiles are generated from a deterministic seed for reproducibility.
"""

import pygame
import random


class TileMap:
    """Renders a grid of colored tiles as the background layer."""

    PALETTE = [
        (34, 120, 50),   # dark green (grass)
        (42, 130, 55),   # medium green
        (28, 100, 42),   # darker green
        (50, 140, 60),   # light green
        (80, 70, 50),    # dirt path
        (90, 80, 55),    # lighter dirt
        (60, 55, 40),    # dark dirt
        (38, 115, 48),   # another green
    ]

    def __init__(self, width, height, tile_size=40, seed=42):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.cols = (width + tile_size - 1) // tile_size
        self.rows = (height + tile_size - 1) // tile_size
        self.seed = seed
        self.surface = None
        self._build_tilemap()

    def _build_tilemap(self):
        """Pre-render the tilemap to a surface for fast blitting."""
        self.surface = pygame.Surface((self.width, self.height))
        rng = random.Random(self.seed)

        for row in range(self.rows):
            for col in range(self.cols):
                color_idx = rng.randint(0, len(self.PALETTE) - 1)
                color = self.PALETTE[color_idx]
                rect = pygame.Rect(
                    col * self.tile_size,
                    row * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(self.surface, color, rect)

                # Add subtle variation with a smaller inner rect
                inner_color = (
                    min(255, color[0] + rng.randint(-8, 8)),
                    min(255, color[1] + rng.randint(-8, 8)),
                    min(255, color[2] + rng.randint(-8, 8)),
                )
                inner_rect = rect.inflate(-4, -4)
                pygame.draw.rect(self.surface, inner_color, inner_rect)

    def render(self, target):
        """Blit the pre-rendered tilemap onto the target surface."""
        target.blit(self.surface, (0, 0))

    def get_tile_color(self, col, row):
        """Get the base color of a specific tile (for game logic)."""
        rng = random.Random(self.seed)
        for _ in range(row * self.cols + col + 1):
            idx = rng.randint(0, len(self.PALETTE) - 1)
        return self.PALETTE[idx]

    def world_to_tile(self, x, y):
        """Convert world coordinates to tile coordinates."""
        return x // self.tile_size, y // self.tile_size

    def tile_to_world(self, col, row):
        """Convert tile coordinates to world coordinates (top-left corner)."""
        return col * self.tile_size, row * self.tile_size
