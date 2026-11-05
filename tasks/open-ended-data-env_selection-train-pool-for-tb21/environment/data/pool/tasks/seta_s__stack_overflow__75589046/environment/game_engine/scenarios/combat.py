"""Combat scenario — entities must handle target destruction gracefully."""

import logging

from engine.vectors import Vector2
from game.systems.targeting import TargetingComponent
from scenarios.base import BaseScenario, ScenarioResult

logger = logging.getLogger("scenario.combat")


class CombatScenario(BaseScenario):
    name = "combat"

    def run(self):
        result = ScenarioResult(self.name)
        self.add_flat_floor()

        enemies = []
        for i in range(5):
            e = self.create_entity(f"Enemy_{i}", Vector2(i * 50, 0))
            e.tags.add("enemy")
            enemies.append(e)

        trackers = []
        for i in range(3):
            t = self.create_entity(f"Tracker_{i}", Vector2(-50 - i * 30, 0))
            t.tags.add("tracker")
            tc = TargetingComponent(t)
            t.set_property("targeting", tc)
            trackers.append((t, tc))

        target = enemies[0]
        for _, tc in trackers:
            tc.acquire(target)

        for _ in range(60):
            for _, tc in trackers:
                tc.tick()
            self.step()

        logger.info("Destroying %s while trackers are locked on", target.name)
        self.entity_manager.remove(target)
        self.entity_manager.flush_destroyed()

        errors = []
        for _ in range(200):
            for _, tc in trackers:
                try:
                    tc.tick()
                except (AttributeError, TypeError) as exc:
                    errors.append(str(exc))
                    logger.error("Tick error after target death: %s", exc)
            self.step()

        for tracker_entity, tc in trackers:
            if tc.target is not None and not tc.target.is_alive:
                errors.append(
                    f"{tracker_entity.name} still holds dead target reference"
                )

        result.details["errors"] = errors
        result.details["error_count"] = len(errors)

        if not errors:
            result.passed = True
            logger.info("Combat: target destruction handled cleanly")
        else:
            result.fail(f"{len(errors)} error(s) during/after target destruction")
            logger.error("Combat FAILED with %d errors", len(errors))

        return result
