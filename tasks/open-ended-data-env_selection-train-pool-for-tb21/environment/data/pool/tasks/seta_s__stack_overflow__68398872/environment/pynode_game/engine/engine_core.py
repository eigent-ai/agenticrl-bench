"""Core engine loop and scene tree management."""

from __future__ import annotations
import logging
from typing import List
from .node import Node
from .input_system import InputEvent, InputPipeline
from .raycaster import Raycaster
from .signal_system import SignalDispatcher
from .cursor_manager import CursorManager

logger = logging.getLogger("pynode.core")


class EngineCore:
    """Manages the scene tree, input pipeline, signal dispatcher, and
    per-frame updates."""

    def __init__(self):
        self.root = Node("Root")
        self.signal_dispatcher = SignalDispatcher(strict_validation=True)
        self.input_pipeline = InputPipeline(self.root)
        self.raycaster = Raycaster(check_layer=1)
        self.cursor_manager = CursorManager()
        self._last_hovered_area = None
        self._interaction_callbacks = {}
        self.event_log: List[dict] = []

    def register_interaction(self, area, callback) -> None:
        """Register a click callback for an Area node."""
        self._interaction_callbacks[id(area)] = callback

    def inject_event(self, event: InputEvent) -> None:
        """Inject an input event into the engine pipeline."""
        logger.info(f"OS-level event: {event}")
        self.event_log.append({
            "type": event.event_type,
            "x": event.x,
            "y": event.y,
        })

        self.input_pipeline.propagate(event)

        if event.consumed:
            logger.debug("Event consumed during propagation")
            return

        if event.event_type == InputEvent.MOUSE_BUTTON_DOWN:
            self._handle_click(event)
        elif event.event_type == InputEvent.MOUSE_MOTION:
            self._handle_hover(event)

    def _handle_click(self, event: InputEvent) -> None:
        hit = self.raycaster.cast(self.root, event.x, event.y)
        if hit is None:
            logger.debug(f"Click at ({event.x},{event.y}): no area hit")
            return
        logger.info(f"Click hit area: {hit.name}")
        self.signal_dispatcher.emit(hit, "clicked", event,
                                    shape_index=str(hit.z_index))
        cb = self._interaction_callbacks.get(id(hit))
        if cb:
            cb(event)

    def _handle_hover(self, event: InputEvent) -> None:
        hit = self.raycaster.cast(self.root, event.x, event.y)
        if hit is not self._last_hovered_area:
            if self._last_hovered_area is not None:
                self.signal_dispatcher.emit(
                    self._last_hovered_area, "mouse_exited",
                    self._last_hovered_area)
            if hit is not None:
                self.signal_dispatcher.emit(hit, "mouse_entered", hit)
            self._last_hovered_area = hit

    def process_frame(self) -> None:
        """Run one simulation frame (overlap detection etc.)."""
        all_nodes = self.root.get_all_descendants()
        from .area import Area
        for node in all_nodes:
            if isinstance(node, Area):
                node._process_overlaps(all_nodes, self.signal_dispatcher)
