"""Interactive game objects: chests, levers, doors."""

from __future__ import annotations
import logging
from engine.area import Area

logger = logging.getLogger("pynode.game.objects")


class Chest(Area):
    def __init__(self, name: str = "Chest",
                 position=(0, 0), size=(40, 40)):
        super().__init__(name, position, size,
                         interaction_layer=2, interaction_mask=1)
        self.opened = False
        self.z_index = 5

    def on_clicked(self, event, shape_index: int = 0):
        self.opened = True
        logger.info(f"{self.name} opened!")


class Lever(Area):
    def __init__(self, name: str = "Lever",
                 position=(0, 0), size=(20, 60)):
        super().__init__(name, position, size,
                         interaction_layer=2, interaction_mask=1)
        self.state = "default"
        self.z_index = 5

    def on_clicked(self, event, shape_index: int = 0):
        self.state = "pulled"
        logger.info(f"{self.name} pulled!")


class Door(Area):
    def __init__(self, name: str = "Door",
                 position=(0, 0), size=(30, 80)):
        super().__init__(name, position, size,
                         interaction_layer=2, interaction_mask=1)
        self.is_open = False
        self.z_index = 5

    def on_clicked(self, event, shape_index: int = 0):
        self.is_open = True
        logger.info(f"{self.name} opened!")
