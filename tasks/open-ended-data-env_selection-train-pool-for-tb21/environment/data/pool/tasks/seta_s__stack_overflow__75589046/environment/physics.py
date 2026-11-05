import math

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def normalized(self):
        mag = math.sqrt(self.x**2 + self.y**2)
        if mag == 0.0:
            return Vector2(0.0, 0.0)
        return Vector2(self.x / mag, self.y / mag)

    def direction_to(self, other):
        return Vector2(other.x - self.x, other.y - self.y).normalized()

    def distance_to(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    def __repr__(self):
        return f"Vector2({self.x:.3f}, {self.y:.3f})"


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def lerp(a, b, t):
    return a + (b - a) * t
