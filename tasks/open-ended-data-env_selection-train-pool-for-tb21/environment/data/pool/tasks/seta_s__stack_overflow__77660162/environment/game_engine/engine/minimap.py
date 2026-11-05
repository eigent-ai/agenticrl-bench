"""Minimap overlay that shows a scaled-down view of the game world.

The minimap composites a scaled version of the main scene with a
translucent border frame, positioned in the corner of the screen.
"""

import pygame


class Minimap:
    """Renders a minimap overlay with translucent border."""

    def __init__(self, x, y, map_width, map_height, border_width=4,
                 border_color=(200, 200, 255, 128)):
        self.x = x
        self.y = y
        self.map_width = map_width
        self.map_height = map_height
        self.border_width = border_width
        self.border_color = border_color
        self.overlay = pygame.Surface((self.map_width, self.map_height))
        self.markers = []

    def add_marker(self, world_x, world_y, color, world_width, world_height):
        """Add a position marker to the minimap.

        Args:
            world_x, world_y: Position in world coordinates.
            color: Marker color as (R, G, B) or (R, G, B, A).
            world_width, world_height: Full world dimensions for scaling.
        """
        map_x = int(world_x / world_width * self.map_width)
        map_y = int(world_y / world_height * self.map_height)
        self.markers.append((map_x, map_y, color))

    def clear_markers(self):
        """Remove all position markers."""
        self.markers.clear()

    def render(self, scene_surface, target):
        """Render the minimap onto the target surface.

        Args:
            scene_surface: The main scene surface to scale down.
            target: The surface to blit the minimap onto.
        """
        inner_w = self.map_width - 2 * self.border_width
        inner_h = self.map_height - 2 * self.border_width

        scaled_scene = pygame.transform.scale(scene_surface, (inner_w, inner_h))

        self.overlay.fill((0, 0, 0, 0))

        pygame.draw.rect(
            self.overlay,
            self.border_color,
            (0, 0, self.map_width, self.map_height)
        )

        self.overlay.blit(scaled_scene, (self.border_width, self.border_width))

        for mx, my, color in self.markers:
            mx = max(self.border_width, min(mx, self.map_width - self.border_width - 1))
            my = max(self.border_width, min(my, self.map_height - self.border_width - 1))
            pygame.draw.circle(self.overlay, color, (mx, my), 3)

        target.blit(self.overlay, (self.x, self.y))

    def get_surface(self):
        """Return the minimap overlay surface for inspection."""
        return self.overlay

    def screen_to_world(self, screen_x, screen_y, world_width, world_height):
        """Convert minimap screen coordinates to world coordinates."""
        local_x = screen_x - self.x - self.border_width
        local_y = screen_y - self.y - self.border_width
        inner_w = self.map_width - 2 * self.border_width
        inner_h = self.map_height - 2 * self.border_width
        if 0 <= local_x < inner_w and 0 <= local_y < inner_h:
            wx = local_x / inner_w * world_width
            wy = local_y / inner_h * world_height
            return wx, wy
        return None
