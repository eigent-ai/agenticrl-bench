"""Parser for desktop environment keyboard shortcut config files.

Supports:
- GNOME dconf INI-style dumps
- XFCE xfconf XML dumps
- MATE dconf INI-style dumps
"""

import os
import re
import configparser
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List


MODIFIER_ALIASES = {
    "Control": "Control",
    "Ctrl": "Control",
    "Alt": "Alt",
    "Shift": "Shift",
    "Super": "Super",
    "Meta": "Alt",
    "Mod1": "Alt",
    "Mod4": "Super",
    "Hyper": "Super",
}

KEYSYM_MAP = {
    "Return": "Return",
    "Escape": "Escape",
    "Tab": "Tab",
    "BackSpace": "BackSpace",
    "Delete": "Delete",
    "Home": "Home",
    "End": "End",
    "Page_Up": "Page_Up",
    "Page_Down": "Page_Down",
    "Left": "Left",
    "Right": "Right",
    "Up": "Up",
    "Down": "Down",
    "space": "space",
    "Print": "Print",
    "Scroll_Lock": "Scroll_Lock",
    "Pause": "Pause",
    "Insert": "Insert",
    "Menu": "Menu",
    "grave": "grave",
    "asciitilde": "asciitilde",
    "F1": "F1",
    "F2": "F2",
    "F3": "F3",
    "F4": "F4",
    "F5": "F5",
    "F6": "F6",
    "F7": "F7",
    "F8": "F8",
    "F9": "F9",
    "F10": "F10",
    "F11": "F11",
    "F12": "F12",
}


@dataclass
class Shortcut:
    """Represents a parsed keyboard shortcut."""
    accelerator: str
    action: str
    source: str
    source_file: str

    def to_dict(self):
        return {
            "accelerator": self.accelerator,
            "action": self.action,
            "source": self.source,
            "source_file": self.source_file,
        }


def resolve_keyname(name):
    """Resolve a key name to its canonical keysym."""
    if name in KEYSYM_MAP:
        return KEYSYM_MAP[name]
    if len(name) == 1:
        return name.lower()
    raise ValueError(f"Unknown keysym: {name}")


def parse_accelerator(accel_string):
    """Parse a GTK accelerator string into (modifiers, key) tuple.

    Examples:
        '<Control>c' -> (['Control'], 'c')
        '<Primary><Alt>t' -> (['Control', 'Alt'], 't')
        '<Above_Tab>' -> ([], 'grave')
    """
    modifiers = []
    remaining = accel_string.strip()

    modifier_pattern = re.compile(r'^<([^>]+)>')

    while True:
        match = modifier_pattern.match(remaining)
        if not match:
            break
        mod_name = match.group(1)

        if mod_name in MODIFIER_ALIASES:
            canonical = MODIFIER_ALIASES[mod_name]
            if canonical not in modifiers:
                modifiers.append(canonical)
            remaining = remaining[match.end():]
        else:
            # Could be a special keysym like Above_Tab wrapped in angle brackets
            try:
                resolved = resolve_keyname(mod_name)
                remaining = resolved + remaining[match.end():]
            except ValueError:
                raise ValueError(f"Unknown modifier: {mod_name}")

    if remaining:
        key = resolve_keyname(remaining)
    else:
        raise ValueError(f"No key found in accelerator: {accel_string}")

    return modifiers, key


def parse_ini_config(filepath, source_name):
    """Parse an INI-style dconf shortcut dump."""
    shortcuts = []
    config = configparser.ConfigParser()
    config.read(filepath)

    for section in config.sections():
        for key, value in config.items(section):
            if key == "name" or key == "action":
                continue
            accel = value.strip().strip("'\"")
            if not accel or accel == "disabled" or accel == "''":
                continue
            action_name = f"{section}/{key}"
            try:
                sc = Shortcut(
                    accelerator=accel,
                    action=action_name,
                    source=source_name,
                    source_file=filepath,
                )
                shortcuts.append(sc)
            except Exception as e:
                print(f"  Warning: skipping {action_name}: {e}")

    return shortcuts


def parse_xfce_xml(filepath, source_name):
    """Parse an XFCE xfconf-style XML shortcut dump."""
    shortcuts = []
    tree = ET.parse(filepath)
    root = tree.getroot()

    for prop in root.iter("property"):
        prop_name = prop.get("name", "")
        prop_type = prop.get("type", "")
        prop_value = prop.get("value", "")

        if prop_type == "string" and prop_value and prop_name.startswith("/"):
            action_name = prop_value
            accel_parts = prop_name.strip("/").split("/")
            if len(accel_parts) >= 1:
                accel_key = accel_parts[-1]
                if "<" in accel_key or len(accel_key) == 1:
                    try:
                        sc = Shortcut(
                            accelerator=accel_key,
                            action=action_name,
                            source=source_name,
                            source_file=filepath,
                        )
                        shortcuts.append(sc)
                    except Exception as e:
                        print(f"  Warning: skipping {prop_name}: {e}")

    return shortcuts


def parse_config_directory(config_dir):
    """Parse all config files in a directory."""
    all_shortcuts = []

    for filename in sorted(os.listdir(config_dir)):
        filepath = os.path.join(config_dir, filename)
        if not os.path.isfile(filepath):
            continue

        if filename == "gnome_shortcuts.ini":
            shortcuts = parse_ini_config(filepath, "gnome")
            all_shortcuts.extend(shortcuts)
        elif filename == "xfce_shortcuts.xml":
            shortcuts = parse_xfce_xml(filepath, "xfce")
            all_shortcuts.extend(shortcuts)
        elif filename == "mate_shortcuts.ini":
            shortcuts = parse_ini_config(filepath, "mate")
            all_shortcuts.extend(shortcuts)
        else:
            print(f"  Skipping unknown file: {filename}")

    return all_shortcuts
