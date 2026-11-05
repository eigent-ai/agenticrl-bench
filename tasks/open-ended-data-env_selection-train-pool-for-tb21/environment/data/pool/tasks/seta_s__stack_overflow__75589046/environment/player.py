from physics import Vector2

class Player:
    def __init__(self, position, alive=True):
        self.position = Vector2(*position)
        self.alive = alive
