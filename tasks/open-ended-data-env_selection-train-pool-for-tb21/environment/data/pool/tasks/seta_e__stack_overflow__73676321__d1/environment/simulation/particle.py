import numpy as np


class Particle:
    """A 2D particle with position, velocity, mass, and rectangular dimensions."""

    def __init__(self, x, y, vx, vy, mass, width, height, density=None):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.mass = float(mass)
        self.width = float(width)
        self.height = float(height)
        if density is not None:
            self.density = float(density)
        else:
            self.density = self.mass / (self.width * self.height)
        self.fx = 0.0
        self.fy = 0.0

    def reset_forces(self):
        self.fx = 0.0
        self.fy = 0.0

    def apply_force(self, fx, fy):
        self.fx += fx
        self.fy += fy

    @property
    def top(self):
        return self.y - self.height / 2.0

    @property
    def bottom(self):
        return self.y + self.height / 2.0

    @property
    def left(self):
        return self.x - self.width / 2.0

    @property
    def right(self):
        return self.x + self.width / 2.0

    @property
    def area(self):
        return self.width * self.height

    @property
    def speed(self):
        return np.sqrt(self.vx ** 2 + self.vy ** 2)

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
            "mass": self.mass,
            "width": self.width,
            "height": self.height,
            "density": self.density,
        }
