"""Inventory system with drag-and-drop items."""

from __future__ import annotations
import logging
from engine.area import Area
from engine.drag_controller import DragController

logger = logging.getLogger("pynode.game.inventory")


class InventorySlot(Area):
    """A single inventory slot that can hold one item."""

    def __init__(self, name: str, position=(0, 0), size=(48, 48),
                 item_name: str = ""):
        super().__init__(name, position, size,
                         interaction_layer=2, interaction_mask=1)
        self.item_name = item_name
        self.z_index = 90

    def has_item(self) -> bool:
        return bool(self.item_name)


class InventoryBar:
    """Manages a row of inventory slots and drag-and-drop."""

    def __init__(self, drag_controller: DragController,
                 slot_count: int = 4, start_x: float = 300,
                 y: float = 550, slot_size: float = 48):
        self.slots = []
        self.drag_controller = drag_controller
        for i in range(slot_count):
            x = start_x + i * (slot_size + 4)
            slot = InventorySlot(
                f"InvSlot_{i}", position=(x, y),
                size=(slot_size, slot_size))
            self.slots.append(slot)

    def set_item(self, slot_index: int, item_name: str) -> None:
        if 0 <= slot_index < len(self.slots):
            self.slots[slot_index].item_name = item_name

    def setup_drag(self, engine_core) -> None:
        """Wire up drag-and-drop for inventory slots."""
        for slot in self.slots:
            def make_drag_starter(s):
                def start(event, shape_index: int = 0):
                    if s.has_item():
                        self.drag_controller.start_drag(
                            s.item_name, event.x, event.y)
                return start
            engine_core.signal_dispatcher.connect(
                slot, "clicked", make_drag_starter(slot))
