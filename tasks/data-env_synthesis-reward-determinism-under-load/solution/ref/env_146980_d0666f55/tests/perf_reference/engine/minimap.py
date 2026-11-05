import pygame
class Minimap:
    def __init__(self, x, y, map_width, map_height, border_width=4,
                 border_color=(200, 200, 255, 128)):
        self.x = x
        self.y = y
        self.map_width = map_width
        self.map_height = map_height
        self.border_width = border_width
        self.border_color = border_color
        self.overlay = pygame.Surface((self.map_width, self.map_height), pygame.SRCALPHA)
        self.markers = []
    def add_marker(self, world_x, world_y, color, world_width, world_height):
        map_x = int(world_x / world_width * self.map_width)
        map_y = int(world_y / world_height * self.map_height)
        self.markers.append((map_x, map_y, color))
    def clear_markers(self):
        self.markers.clear()
    def render(self, scene_surface, target):
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
        return self.overlay
    def screen_to_world(self, screen_x, screen_y, world_width, world_height):
        local_x = screen_x - self.x - self.border_width
        local_y = screen_y - self.y - self.border_width
        inner_w = self.map_width - 2 * self.border_width
        inner_h = self.map_height - 2 * self.border_width
        if 0 <= local_x < inner_w and 0 <= local_y < inner_h:
            wx = local_x / inner_w * world_width
            wy = local_y / inner_h * world_height
            return wx, wy
        return None
