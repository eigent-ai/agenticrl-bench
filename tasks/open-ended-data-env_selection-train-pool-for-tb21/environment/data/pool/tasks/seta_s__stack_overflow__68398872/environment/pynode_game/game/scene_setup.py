"""Scene tree construction and signal wiring."""

from __future__ import annotations
import logging
from engine.engine_core import EngineCore
from engine.node import Node
from engine.drag_controller import DragController
from engine.cursor_manager import CursorManager
from .interactive_objects import Chest, Lever, Door
from .player import Player
from .trigger_zones import FlagZone, CheckpointZone
from .hud import HUD
from .inventory import InventoryBar

logger = logging.getLogger("pynode.game.scene")


def build_scene(engine: EngineCore):
    """Construct the full scene tree and wire all signals."""

    game_world = Node("GameWorld")
    game_world.z_index = 0
    engine.root.add_child(game_world)

    background = Node("Background")
    background.z_index = 0
    game_world.add_child(background)

    chest = Chest("TreasureChest", position=(100, 200), size=(40, 40))
    lever = Lever("WallLever", position=(300, 150), size=(20, 60))
    door = Door("IronDoor", position=(500, 100), size=(30, 80))
    game_world.add_child(chest)
    game_world.add_child(lever)
    game_world.add_child(door)

    engine.register_interaction(chest, chest.on_clicked)
    engine.register_interaction(lever, lever.on_clicked)
    engine.register_interaction(door, door.on_clicked)

    engine.signal_dispatcher.connect(chest, "clicked", chest.on_clicked)
    engine.signal_dispatcher.connect(lever, "clicked", lever.on_clicked)
    engine.signal_dispatcher.connect(door, "clicked", door.on_clicked)

    player = Player(position=(50, 300))
    game_world.add_child(player)

    flag_zone = FlagZone("FlagAlpha", position=(400, 280), size=(60, 60))
    checkpoint_zone = CheckpointZone("Checkpoint1", position=(600, 280),
                                     size=(60, 60))
    game_world.add_child(flag_zone)
    game_world.add_child(checkpoint_zone)

    engine.signal_dispatcher.connect(
        flag_zone, "body_entered",
        lambda body, shape_index=0: (
            flag_zone.on_body_entered(body, shape_index),
            player.on_flag(flag_zone),
        )
    )
    engine.signal_dispatcher.connect(
        checkpoint_zone, "body_entered",
        lambda body, shape_index=0: (
            checkpoint_zone.on_body_entered(body, shape_index),
            player.on_checkpoint(checkpoint_zone),
        )
    )

    hud = HUD(screen_width=800, screen_height=600)
    engine.root.add_child(hud)

    drag_controller = DragController("DragCtrl")
    engine.root.add_child(drag_controller)

    inventory = InventoryBar(drag_controller, slot_count=4,
                             start_x=300, y=550, slot_size=48)
    for slot in inventory.slots:
        game_world.add_child(slot)
    inventory.set_item(0, "rusty_key")
    inventory.set_item(1, "magic_gem")
    inventory.setup_drag(engine)

    drag_controller.on_drop = lambda item, x, y: logger.info(
        f"Item {item} dropped at ({x},{y})")

    for area in [chest, lever, door]:
        engine.cursor_manager.register_area(area)
        engine.signal_dispatcher.connect(
            area, "mouse_entered",
            engine.cursor_manager.onMouseEnteredArea
        )
        engine.signal_dispatcher.connect(
            area, "mouse_exited",
            engine.cursor_manager.onMouseExitedArea
        )

    return {
        "game_world": game_world,
        "chest": chest,
        "lever": lever,
        "door": door,
        "player": player,
        "flag_zone": flag_zone,
        "checkpoint_zone": checkpoint_zone,
        "hud": hud,
        "drag_controller": drag_controller,
        "inventory": inventory,
    }
