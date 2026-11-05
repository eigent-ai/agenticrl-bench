"""Area node -- detects overlaps and receives targeted input events."""

from __future__ import annotations
from typing import Tuple
from .node import Node


class Area(Node):
    """An invisible region that detects overlaps and can receive input."""

    def __init__(self, name: str = "Area",
                 position: Tuple[float, float] = (0, 0),
                 size: Tuple[float, float] = (50, 50),
                 interaction_layer: int = 2,
                 interaction_mask: int = 1):
        super().__init__(name)
        self.position = position
        self.size = size
        self.interaction_layer = interaction_layer
        self.interaction_mask = interaction_mask
        self.monitoring = True
        self._overlapping_bodies = set()
        self._overlapping_areas = set()

    def contains_point(self, x: float, y: float) -> bool:
        px, py = self.position
        sx, sy = self.size
        return px <= x <= px + sx and py <= y <= py + sy

    def check_overlap(self, other_node: Node) -> bool:
        """Check AABB overlap with another node that has position/size."""
        if not self.monitoring:
            return False
        if not hasattr(other_node, "position") or not hasattr(other_node, "size"):
            return False
        ox, oy = other_node.position
        osx, osy = other_node.size
        ax, ay = self.position
        asx, asy = self.size
        return (ax < ox + osx and ax + asx > ox and
                ay < oy + osy and ay + asy > oy)

    def _process_overlaps(self, all_nodes, signal_dispatcher):
        """Called each frame to detect enter/exit of bodies and areas."""
        from .physics_body import PhysicsBody
        currently_overlapping_bodies = set()
        currently_overlapping_areas = set()
        for node in all_nodes:
            if node is self:
                continue
            if self.check_overlap(node):
                if isinstance(node, PhysicsBody):
                    currently_overlapping_bodies.add(node)
                elif isinstance(node, Area):
                    currently_overlapping_areas.add(node)

        new_bodies = currently_overlapping_bodies - self._overlapping_bodies
        for body in new_bodies:
            signal_dispatcher.emit(self, "area_entered", body, shape_index=0)

        new_areas = currently_overlapping_areas - self._overlapping_areas
        for area in new_areas:
            signal_dispatcher.emit(self, "area_entered", area, shape_index=0)

        exited_bodies = self._overlapping_bodies - currently_overlapping_bodies
        for body in exited_bodies:
            signal_dispatcher.emit(self, "area_exited", body, shape_index=0)

        exited_areas = self._overlapping_areas - currently_overlapping_areas
        for area in exited_areas:
            signal_dispatcher.emit(self, "area_exited", area, shape_index=0)

        self._overlapping_bodies = currently_overlapping_bodies
        self._overlapping_areas = currently_overlapping_areas
