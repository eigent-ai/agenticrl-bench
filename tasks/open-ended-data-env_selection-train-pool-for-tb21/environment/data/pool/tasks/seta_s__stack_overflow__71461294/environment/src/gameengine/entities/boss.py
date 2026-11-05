"""Boss monster entity - diamond inheritance from Monster and EliteEntity."""

from gameengine.entities.monster import Monster
from gameengine.entities.elite import EliteEntity
from gameengine.entities.base import ComponentMixin


class BossMonster(Monster, EliteEntity, ComponentMixin):
    """A powerful boss monster with both resistance and shield mechanics.

    Inherits from both Monster (resistance) and EliteEntity (shield).
    """

    def __init__(self, name, hp=500, attack=25, defense=15, **kwargs):
        kwargs.setdefault("resistance", 0.3)
        kwargs.setdefault("shield", 50)
        super().__init__(name, hp=hp, attack=attack, defense=defense, **kwargs)
        self.__init_components__()
        self.phase = 1
        self.enrage_threshold = kwargs.get("enrage_threshold", 0.25)
        self.abilities = kwargs.get("abilities", ["slam", "roar"])
        self.entity_type = "boss_monster"

    def update(self, world_state):
        """Boss update with phase transitions."""
        super().update(world_state)
        hp_ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
        if hp_ratio <= self.enrage_threshold and self.phase == 1:
            self.phase = 2
            self.attack = int(self.attack * 1.5)

    def get_info(self):
        info = super().get_info()
        info.update({
            "phase": self.phase,
            "abilities": self.abilities,
            "resistance": self.resistance,
            "shield": self.shield,
            "components": self.get_all_components(),
        })
        return info

    def interact(self, target, action_type):
        if action_type == "attack":
            return {"type": "boss_combat", "attacker": self.name, "target": target.name, "phase": self.phase}
        return {"type": "boss_roar", "source": self.name}
