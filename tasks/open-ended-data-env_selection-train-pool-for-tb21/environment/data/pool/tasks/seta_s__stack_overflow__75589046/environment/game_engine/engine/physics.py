"""Tick-based 2D physics engine.

Handles gravity, floor/slope collisions, and the move_and_slide pattern
used by entities that need to interact with the world geometry.
"""

import math
import logging

from engine.vectors import Vector2

logger = logging.getLogger("physics")

TICK_RATE = 60
DT = 1.0 / TICK_RATE


class FloorSurface:
    """A line-segment floor that entities can stand on."""

    def __init__(self, x_start, x_end, y_start, y_end):
        self.x_start = float(x_start)
        self.x_end = float(x_end)
        self.y_start = float(y_start)
        self.y_end = float(y_end)

        dx = self.x_end - self.x_start
        dy = self.y_end - self.y_start
        seg_len = math.sqrt(dx * dx + dy * dy)
        if seg_len < 1e-12:
            self.normal = Vector2.up()
        else:
            self.normal = Vector2(-dy / seg_len, dx / seg_len)
            if self.normal.y < 0:
                self.normal = -self.normal

        self.angle = math.acos(
            min(1.0, max(-1.0, self.normal.dot(Vector2.up())))
        )

    def height_at(self, x):
        if x < self.x_start or x > self.x_end:
            return None
        if abs(self.x_end - self.x_start) < 1e-12:
            return self.y_start
        t = (x - self.x_start) / (self.x_end - self.x_start)
        return self.y_start + t * (self.y_end - self.y_start)


class PhysicsWorld:
    """Global physics state: surfaces, gravity config, constants."""

    def __init__(self, config=None):
        config = config or {}
        self.jump_gravity = float(config.get("jump_gravity", 20.0))
        self.fall_gravity = float(config.get("fall_gravity", 30.0))
        self.floor_max_angle = math.radians(
            float(config.get("floor_max_angle_degrees", 55))
        )
        self.surfaces = []

    def add_surface(self, surface):
        self.surfaces.append(surface)

    def get_floor_at(self, x):
        """Return (height, surface) of the highest floor at *x*, or None."""
        best_h = None
        best_s = None
        for s in self.surfaces:
            h = s.height_at(x)
            if h is not None and (best_h is None or h > best_h):
                best_h = h
                best_s = s
        if best_h is not None:
            return best_h, best_s
        return None

    def get_gravity(self, velocity):
        """Return gravity magnitude for current vertical velocity.

        Positive y is up in this engine.  Ascending (velocity.y > 0) should
        use jump_gravity; descending (velocity.y <= 0) should use
        fall_gravity — giving the classic asymmetric jump arc.
        """
        if velocity.y < 0:
            return self.jump_gravity
        else:
            return self.fall_gravity


class PhysicsBody:
    """Gives an entity physics-aware movement (gravity + collision)."""

    def __init__(self, entity, world):
        self.entity = entity
        self.world = world
        self._on_floor = False
        self._floor_normal = Vector2.up()
        self._floor_surface = None

    def is_on_floor(self):
        return self._on_floor

    def get_floor_normal(self):
        return self._floor_normal

    def move_and_slide(self, velocity):
        """Move by *velocity* for one tick, slide along floors."""
        self.entity.position = self.entity.position + velocity * DT

        floor_info = self.world.get_floor_at(self.entity.position.x)
        if floor_info is not None:
            floor_height, surface = floor_info
            if self.entity.position.y <= floor_height + 0.01:
                self.entity.position = Vector2(
                    self.entity.position.x, floor_height
                )
                self._on_floor = True
                self._floor_normal = surface.normal
                self._floor_surface = surface

                if velocity.dot(surface.normal) < 0:
                    normal_comp = velocity.dot(surface.normal)
                    velocity = velocity - surface.normal * normal_comp
            else:
                self._on_floor = False
                self._floor_surface = None
        else:
            self._on_floor = False
            self._floor_surface = None

        self.entity.velocity = velocity.copy()
        return velocity

    def physics_process(self, input_velocity=None):
        """Run one full physics tick: apply gravity, move, resolve."""
        input_velocity = input_velocity or Vector2.zero()

        gravity_mag = self.world.get_gravity(self.entity.velocity)
        gravity_accel = Vector2(0, -gravity_mag)

        self.entity.velocity = self.entity.velocity + gravity_accel * DT

        self.move_and_slide(self.entity.velocity)

        if input_velocity.length_squared() > 1e-12:
            self.entity.velocity = self.entity.velocity + input_velocity
            self.move_and_slide(self.entity.velocity)
