"""Input raycaster -- determines which Area node a mouse event targets."""

from __future__ import annotations
import logging
from typing import Optional, List
from .node import Node
from .area import Area

logger = logging.getLogger("pynode.raycaster")


class Raycaster:
    """Casts a ray at a screen position and returns the topmost Area that
    matches the configured interaction layers."""

    def __init__(self, check_layer: int = 1):
        self.check_layer = check_layer

    def cast(self, root: Node, x: float, y: float) -> Optional[Area]:
        """Find the front-most Area at (x, y) whose interaction_layer
        matches our check_layer."""
        candidates = self._collect_areas(root)
        candidates.sort(key=lambda a: a.z_index, reverse=True)

        for area in candidates:
            if not area.contains_point(x, y):
                continue
            if area.interaction_layer & self.check_layer:
                logger.debug(f"Raycast hit: {area.name} at ({x},{y})")
                return area
            else:
                logger.debug(
                    f"Raycast skipped {area.name}: layer {area.interaction_layer} "
                    f"does not match check_layer {self.check_layer}"
                )
        return None

    def _collect_areas(self, node: Node) -> List[Area]:
        result = []
        if isinstance(node, Area):
            result.append(node)
        for child in node.children:
            result.extend(self._collect_areas(child))
        return result
