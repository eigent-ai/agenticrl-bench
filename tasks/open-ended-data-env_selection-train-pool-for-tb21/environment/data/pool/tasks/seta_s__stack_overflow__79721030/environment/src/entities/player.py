from .base import Entity


class Player(Entity):
    def initialize(self, x=0, y=0, width=16, height=16, speed=100):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.speed = speed
        self.color = (0, 0, 255)
        self.sprite_width = width
        self.sprite_height = height
        self.scale_x = 1.0
        self.scale_y = 1.0
