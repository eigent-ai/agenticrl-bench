"""AI behavior trees for game entities."""


class BehaviorTree:
    """Simple behavior tree for entity AI."""

    def __init__(self, entity):
        self.entity = entity
        self.actions = []

    def tick(self, world_state):
        """Execute one AI tick and return the chosen action."""
        raise NotImplementedError


class PatrolBehavior(BehaviorTree):
    """Patrol behavior for NPCs."""

    def tick(self, world_state):
        entity = self.entity
        if not entity.alive:
            return {"action": "dead", "entity": entity.name}

        entity.advance_patrol()
        patrol_state = entity.get_patrol_state()
        action = {
            "action": "patrol",
            "entity": entity.name,
            "position": patrol_state["position"],
            "state": patrol_state["state"],
        }
        self.actions.append(action)
        return action


class CombatBehavior(BehaviorTree):
    """Combat behavior for monsters."""

    def tick(self, world_state):
        entity = self.entity
        if not entity.alive:
            return {"action": "dead", "entity": entity.name}

        nearby_npcs = [e for e in world_state.get("nearby_entities", [])
                       if hasattr(e, "get_patrol_state") and e.alive]

        npc_states = {}
        for npc in nearby_npcs:
            patrol_state = npc.get_patrol_state()
            npc_states[npc.name] = patrol_state

        if entity.target and entity.target.alive:
            action = {
                "action": "attack",
                "entity": entity.name,
                "target": entity.target.name,
                "npc_awareness": npc_states,
            }
        else:
            action = {
                "action": "idle",
                "entity": entity.name,
                "npc_awareness": npc_states,
            }

        self.actions.append(action)
        return action
