"""Interaction system using the Interactable protocol."""

from gameengine.entities.protocols import Interactable, check_interactable, InteractionResult


class InteractionSystem:
    """Manages interactions between entities."""

    def __init__(self):
        self.interaction_log = []

    def process_interaction(self, source, target, action_type="talk"):
        """Process an interaction between two entities."""
        check_interactable(source)

        result = source.interact(target)
        self.interaction_log.append({
            "source": source.name,
            "target": target.name,
            "action": action_type,
            "result": result if isinstance(result, dict) else result.to_dict() if hasattr(result, "to_dict") else str(result),
        })
        return result

    def get_log(self):
        return list(self.interaction_log)
