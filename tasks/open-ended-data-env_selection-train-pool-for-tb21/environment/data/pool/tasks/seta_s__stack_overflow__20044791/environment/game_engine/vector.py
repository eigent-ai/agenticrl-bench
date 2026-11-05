import math


class Vec2:
    """2D vector with basic math operations."""

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __eq__(self, other):
        if not isinstance(other, Vec2):
            return NotImplemented
        return math.isclose(self.x, other.x, abs_tol=1e-9) and math.isclose(self.y, other.y, abs_tol=1e-9)

    def magnitude(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        m = self.magnitude()
        if m == 0:
            return Vec2(0, 0)
        return Vec2(self.x / m, self.y / m)

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Vec2({self.x:.4f}, {self.y:.4f})"
