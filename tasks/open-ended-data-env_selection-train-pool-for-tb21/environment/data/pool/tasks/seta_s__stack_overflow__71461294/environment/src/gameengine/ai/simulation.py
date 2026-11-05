"""AI simulation runner."""

from gameengine.ai.behavior import PatrolBehavior, CombatBehavior
from gameengine.entities.npc import NPC
from gameengine.entities.monster import Monster


class AISimulation:
    """Runs a multi-tick AI simulation for all entities."""

    def __init__(self, entities, max_ticks=20):
        self.entities = entities
        self.max_ticks = max_ticks
        self.behaviors = {}
        self.tick_log = []
        self._setup_behaviors()

    def _setup_behaviors(self):
        for entity in self.entities:
            if isinstance(entity, Monster):
                self.behaviors[entity.name] = CombatBehavior(entity)
            elif isinstance(entity, NPC):
                self.behaviors[entity.name] = PatrolBehavior(entity)

    def run(self):
        """Run the simulation for max_ticks or until completion."""
        world_state = {"nearby_entities": self.entities}

        for tick in range(self.max_ticks):
            tick_actions = []

            for entity in self.entities:
                if not entity.alive:
                    continue
                entity.update(world_state)

            for name, behavior in self.behaviors.items():
                entity = behavior.entity
                if not entity.alive:
                    continue

                if isinstance(entity, Monster):
                    npc_entities = [e for e in self.entities if isinstance(e, NPC) and e.alive]
                    needs_npc_data = True
                    for npc in npc_entities:
                        ps = npc.get_patrol_state()
                        if ps["state"] == "idle" and npc.ai_actions_processed == 0:
                            needs_npc_data = True

                action = behavior.tick(world_state)
                tick_actions.append(action)

            self.tick_log.append({
                "tick": tick,
                "actions": tick_actions,
            })

        report = {
            "total_ticks": len(self.tick_log),
            "entity_count": len(self.entities),
            "entity_summary": {},
            "tick_log": self.tick_log,
        }

        for entity in self.entities:
            info = entity.get_info()
            report["entity_summary"][entity.name] = {
                "type": info["type"],
                "alive": info["alive"],
                "final_hp": info["hp"],
            }

        return report
