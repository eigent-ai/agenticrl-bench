"""Base Node class for the PyNode Engine scene tree."""

from __future__ import annotations
from typing import Optional, List


class Node:
    """Base scene tree node. All engine objects derive from this."""

    def __init__(self, name: str = "Node"):
        self.name: str = name
        self.parent: Optional[Node] = None
        self.children: List[Node] = []
        self._process_input_enabled: bool = False
        self.z_index: int = 0
        self.visible: bool = True

    # ------------------------------------------------------------------
    # Tree manipulation
    # ------------------------------------------------------------------
    def add_child(self, child: "Node") -> None:
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: "Node") -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def get_node(self, path: str) -> Optional["Node"]:
        """Simple path-based lookup (e.g. 'HUD/HealthBar')."""
        parts = path.split("/")
        current = self
        for part in parts:
            found = None
            for c in current.children:
                if c.name == part:
                    found = c
                    break
            if found is None:
                return None
            current = found
        return current

    # ------------------------------------------------------------------
    # Traversal helpers
    # ------------------------------------------------------------------
    def get_all_descendants(self) -> List["Node"]:
        result = []
        for child in self.children:
            result.append(child)
            result.extend(child.get_all_descendants())
        return result

    def get_children_sorted_for_rendering(self) -> List["Node"]:
        """Return children sorted by z_index ascending (back-to-front)."""
        return sorted(self.children, key=lambda n: n.z_index)

    def get_children_sorted_for_input(self) -> List["Node"]:
        """Return children sorted for input processing."""
        return sorted(self.children, key=lambda n: n.z_index)

    # ------------------------------------------------------------------
    # Input callbacks (overridden by subclasses)
    # ------------------------------------------------------------------
    def _input(self, event) -> bool:
        """Global input handler. Return True to consume the event."""
        return False

    def _input_event(self, event) -> bool:
        """Per-node input handler (only called when event targets this node).
        Return True to consume the event."""
        return False

    def set_process_input(self, enabled: bool) -> None:
        self._process_input_enabled = enabled

    def is_processing_input(self) -> bool:
        return self._process_input_enabled

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
