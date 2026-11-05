"""2D Vector math library for the game engine.

Provides a Vector2 class with standard operations used throughout
the physics and game simulation systems.
"""

import math


class Vector2:
    """Immutable-style 2D vector with common operations."""

    __slots__ = ("x", "y")

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    # ── arithmetic ──────────────────────────────────────────────

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    # ── comparison ──────────────────────────────────────────────

    def __eq__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9

    def __hash__(self):
        return hash((round(self.x, 9), round(self.y, 9)))

    def __repr__(self):
        return f"Vector2({self.x:.4f}, {self.y:.4f})"

    def __bool__(self):
        return self.length_squared() > 1e-18

    # ── properties ──────────────────────────────────────────────

    def length_squared(self):
        return self.x * self.x + self.y * self.y

    def length(self):
        return math.sqrt(self.length_squared())

    def normalized(self):
        """Return a unit-length copy of this vector."""
        mag = self.length()
        return Vector2(self.x / mag, self.y / mag)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def angle(self):
        return math.atan2(self.y, self.x)

    def angle_to(self, other):
        return math.atan2(self.cross(other), self.dot(other))

    def distance_to(self, other):
        return (other - self).length()

    def direction_to(self, other):
        return (other - self).normalized()

    def lerp(self, other, t):
        return self + (other - self) * t

    def rotated(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
        )

    def copy(self):
        return Vector2(self.x, self.y)

    def sign(self):
        """Return a vector with the sign of each component."""
        def _s(v):
            if v > 0:
                return 1.0
            elif v < 0:
                return -1.0
            return 0.0
        return Vector2(_s(self.x), _s(self.y))

    # ── class-level constants ───────────────────────────────────

    @staticmethod
    def zero():
        return Vector2(0.0, 0.0)

    @staticmethod
    def one():
        return Vector2(1.0, 1.0)

    @staticmethod
    def up():
        return Vector2(0.0, 1.0)

    @staticmethod
    def down():
        return Vector2(0.0, -1.0)

    @staticmethod
    def right():
        return Vector2(1.0, 0.0)

    @staticmethod
    def left():
        return Vector2(-1.0, 0.0)
