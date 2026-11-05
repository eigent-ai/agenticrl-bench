import pygame
import random
class TileMap:
    PALETTE = [
        (34, 120, 50),
        (42, 130, 55),
        (28, 100, 42),
        (50, 140, 60),
        (80, 70, 50),
        (90, 80, 55),
        (60, 55, 40),
        (38, 115, 48),
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
                inner_color = (
                    min(255, color[0] + rng.randint(-8, 8)),
                    min(255, color[1] + rng.randint(-8, 8)),
                    min(255, color[2] + rng.randint(-8, 8)),
                )
                inner_rect = rect.inflate(-4, -4)
                pygame.draw.rect(self.surface, inner_color, inner_rect)
    def render(self, target):
        target.blit(self.surface, (0, 0))
    def get_tile_color(self, col, row):
        rng = random.Random(self.seed)
        for _ in range(row * self.cols + col + 1):
            idx = rng.randint(0, len(self.PALETTE) - 1)
        return self.PALETTE[idx]
    def world_to_tile(self, x, y):
        return x // self.tile_size, y // self.tile_size
    def tile_to_world(self, col, row):
        return col * self.tile_size, row * self.tile_size
