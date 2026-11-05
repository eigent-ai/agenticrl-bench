import math


class Camera:
    def __init__(self, viewport_width, viewport_height):
        self.x = 0.0
        self.y = 0.0
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.target = None

    def set_target(self, entity):
        self.target = entity

    def update(self):
        if self.target is not None:
            self.x = math.floor(self.target.x) - self.viewport_width / 2
            self.y = math.floor(self.target.y) - self.viewport_height / 2

    def get_offset(self):
        return self.x, self.y
