"""Targeting system — lets entities acquire and track targets.

When an entity acquires a target, it stores a reference to that
target and uses it each tick for AI decisions (chase, attack, etc.).
"""

import logging

logger = logging.getLogger("targeting")


class TargetingComponent:
    """Attach to an entity so it can lock onto another entity."""

    def __init__(self, entity):
        self.entity = entity
        self._target = None

    @property
    def target(self):
        return self._target

    def acquire(self, target_entity):
        """Set *target_entity* as our current target."""
        if self._target is target_entity:
            return
        self._target = target_entity
        logger.info(
            "%s acquired target %s", self.entity.name, target_entity.name
        )

    def release(self):
        """Drop the current target."""
        if self._target is not None:
            logger.info(
                "%s released target %s",
                self.entity.name,
                getattr(self._target, "name", "<dead>"),
            )
        self._target = None

    def tick(self):
        """Per-tick update — uses target position for AI, etc."""
        if self._target is None:
            return

        if not self._target.is_alive:
            target_name = getattr(self._target, "name", "<unknown>")
            logger.warning(
                "%s's target %s is dead but reference was not cleaned up",
                self.entity.name,
                target_name,
            )
            pos = self._target.position
            _ = pos.x
            return

        dist = self.entity.position.distance_to(self._target.position)
        logger.debug(
            "%s tracking %s at distance %.1f",
            self.entity.name, self._target.name, dist,
        )
