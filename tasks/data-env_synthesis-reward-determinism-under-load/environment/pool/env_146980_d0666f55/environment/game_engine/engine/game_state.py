"""Game state management.

Tracks player position, entities, damage events, and other game data
that drives the rendering engine. This module handles game logic
independently of the rendering system.
"""

import math
import random


class Entity:
    """A game entity with position, health, and type."""

    def __init__(self, entity_id, x, y, entity_type="npc", health=100):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.entity_type = entity_type
        self.health = health
        self.max_health = health
        self.alive = True
        self.speed = 2.0

    def distance_to(self, other_x, other_y):
        """Calculate distance to a point."""
        dx = self.x - other_x
        dy = self.y - other_y
        return math.sqrt(dx * dx + dy * dy)

    def move_toward(self, target_x, target_y):
        """Move entity toward a target position."""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.x += (dx / dist) * min(self.speed, dist)
            self.y += (dy / dist) * min(self.speed, dist)

    def take_damage(self, amount):
        """Apply damage to the entity."""
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.alive = False
        return self.health


class DamageEvent:
    """Records a damage event for floating text display."""

    def __init__(self, x, y, amount, color=(255, 80, 80)):
        self.x = x
        self.y = y
        self.amount = amount
        self.color = color
        self.timestamp = 0


class GameState:
    """Central game state tracking all entities and events."""

    def __init__(self, world_width, world_height, seed=42):
        self.world_width = world_width
        self.world_height = world_height
        self.rng = random.Random(seed)
        self.player_x = world_width // 2
        self.player_y = world_height // 2
        self.player_health = 85
        self.player_max_health = 100
        self.player_mana = 60
        self.player_max_mana = 100
        self.score = 1250
        self.entities = []
        self.damage_events = []
        self.reveal_radius = 80
        self.tick_count = 0
        self._spawn_initial_entities()

    def _spawn_initial_entities(self):
        """Create starting entities at random positions."""
        for i in range(15):
            x = self.rng.randint(50, self.world_width - 50)
            y = self.rng.randint(50, self.world_height - 50)
            entity_type = self.rng.choice(["enemy", "npc", "ally"])
            health = self.rng.randint(50, 200)
            self.entities.append(Entity(i, x, y, entity_type, health))

    def update(self):
        """Advance game state by one tick."""
        self.tick_count += 1

        for entity in self.entities:
            if not entity.alive:
                continue
            if entity.entity_type == "enemy":
                entity.move_toward(self.player_x, self.player_y)
                if entity.distance_to(self.player_x, self.player_y) < 30:
                    dmg = self.rng.randint(5, 15)
                    self.player_health = max(0, self.player_health - dmg)
                    self.damage_events.append(
                        DamageEvent(self.player_x, self.player_y - 20, dmg,
                                    (255, 80, 80))
                    )
            elif entity.entity_type == "npc":
                angle = self.rng.uniform(0, 2 * math.pi)
                entity.x += math.cos(angle) * 0.5
                entity.y += math.sin(angle) * 0.5
                entity.x = max(0, min(self.world_width, entity.x))
                entity.y = max(0, min(self.world_height, entity.y))

    def get_reveal_points(self):
        """Get list of fog-of-war reveal points as (x, y, radius) tuples."""
        points = [(self.player_x, self.player_y, self.reveal_radius)]
        for entity in self.entities:
            if entity.alive and entity.entity_type == "ally":
                points.append((int(entity.x), int(entity.y),
                               self.reveal_radius // 2))
        return points

    def get_entity_positions(self):
        """Get all entity positions for minimap display."""
        positions = []
        for entity in self.entities:
            if entity.alive:
                color = {
                    "enemy": (255, 50, 50),
                    "npc": (200, 200, 100),
                    "ally": (50, 200, 50),
                }.get(entity.entity_type, (200, 200, 200))
                positions.append((entity.x, entity.y, color))
        return positions

    def get_damage_events(self):
        """Get and clear pending damage events for text rendering."""
        events = self.damage_events[:]
        self.damage_events.clear()
        return events

    def move_player(self, dx, dy):
        """Move the player by a delta."""
        self.player_x = max(0, min(self.world_width, self.player_x + dx))
        self.player_y = max(0, min(self.world_height, self.player_y + dy))

    def get_entities_in_radius(self, x, y, radius):
        """Find all living entities within a radius of a point."""
        result = []
        for entity in self.entities:
            if entity.alive and entity.distance_to(x, y) <= radius:
                result.append(entity)
        return result

    def apply_aoe_damage(self, x, y, radius, damage):
        """Apply area-of-effect damage to all entities in range."""
        hit_count = 0
        for entity in self.entities:
            if entity.alive and entity.distance_to(x, y) <= radius:
                entity.take_damage(damage)
                self.damage_events.append(
                    DamageEvent(entity.x, entity.y - 10, damage, (255, 180, 50))
                )
                self.score += damage
                hit_count += 1
        return hit_count
