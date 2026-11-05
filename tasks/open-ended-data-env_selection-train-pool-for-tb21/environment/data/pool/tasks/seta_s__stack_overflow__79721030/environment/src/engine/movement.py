import math


class MovementSystem:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height

    def process(self, entity, dx, dy, dt):
        speed = entity.speed

        new_x = entity.x + dx * speed * dt
        new_y = entity.y + dy * speed * dt

        max_x = self.map_width - entity.width
        max_y = self.map_height - entity.height

        if new_x < 0:
            new_x = -new_x
        elif new_x > max_x:
            new_x = max_x - (new_x - max_x)

        if new_y < 0:
            new_y = -new_y
        elif new_y > max_y:
            new_y = max_y - (new_y - max_y)

        entity.x = new_x
        entity.y = new_y
