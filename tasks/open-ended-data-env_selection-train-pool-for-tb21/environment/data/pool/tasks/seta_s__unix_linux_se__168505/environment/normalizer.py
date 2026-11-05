"""Normalizer for keyboard shortcuts.

Converts parsed shortcuts to canonical form with consistent
modifier ordering and resolved key names.
"""

from dataclasses import dataclass
from typing import List
from parser import parse_accelerator


@dataclass
class NormalizedShortcut:
    """A shortcut in canonical normalized form."""
    original_accelerator: str
    normalized_accelerator: str
    action: str
    source: str
    source_file: str

    def to_dict(self):
        return {
            "original_accelerator": self.original_accelerator,
            "normalized_accelerator": self.normalized_accelerator,
            "action": self.action,
            "source": self.source,
            "source_file": self.source_file,
        }


def normalize_modifiers(modifiers):
    """Normalize modifier list to canonical order.

    Returns modifiers sorted in canonical form.
    """
    return sorted(modifiers)


def build_normalized_accelerator(modifiers, key):
    """Build a normalized accelerator string from modifiers and key."""
    parts = [f"<{m}>" for m in modifiers]
    parts.append(key)
    return "".join(parts)


def normalize_shortcuts(shortcuts):
    """Normalize a list of Shortcut objects to canonical form."""
    normalized = []

    for sc in shortcuts:
        try:
            modifiers, key = parse_accelerator(sc.accelerator)
            norm_mods = normalize_modifiers(modifiers)
            norm_accel = build_normalized_accelerator(norm_mods, key)

            ns = NormalizedShortcut(
                original_accelerator=sc.accelerator,
                normalized_accelerator=norm_accel,
                action=sc.action,
                source=sc.source,
                source_file=sc.source_file,
            )
            normalized.append(ns)
        except ValueError as e:
            print(f"  Warning: could not normalize '{sc.accelerator}' from {sc.source}: {e}")

    return normalized
