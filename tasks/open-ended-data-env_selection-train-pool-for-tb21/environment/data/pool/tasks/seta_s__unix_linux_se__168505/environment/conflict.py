"""Conflict detection for keyboard shortcuts.

Identifies shortcuts that map to the same key combination
but different actions across different config sources.
"""

from dataclasses import dataclass, field
from typing import List
from collections import defaultdict


@dataclass
class ConflictGroup:
    """A group of shortcuts that conflict with each other."""
    normalized_accelerator: str
    entries: list = field(default_factory=list)

    def to_dict(self):
        return {
            "normalized_accelerator": self.normalized_accelerator,
            "entries": [
                {
                    "action": e.action,
                    "source": e.source,
                    "original_accelerator": e.original_accelerator,
                }
                for e in self.entries
            ],
        }


def find_conflicts(normalized_shortcuts):
    """Find conflicting shortcuts across different sources.

    Two shortcuts conflict if they have the same key combination
    but are bound to different actions in different sources.
    """
    # Group by accelerator string
    groups = defaultdict(list)
    for ns in normalized_shortcuts:
        groups[ns.original_accelerator].append(ns)

    conflicts = []
    for accel, entries in groups.items():
        # Check if there are entries from different sources
        sources = set(e.source for e in entries)
        actions = set(e.action for e in entries)

        if len(sources) > 1 and len(actions) > 1:
            cg = ConflictGroup(
                normalized_accelerator=accel,
                entries=entries,
            )
            conflicts.append(cg)

    return conflicts
