import json
from .node import SceneNode
from .query import register_node, clear_registry


def _build_node(data, parent=None):
    node = SceneNode(
        name=data["name"],
        tag=data.get("tag", "Untagged"),
        layer=data.get("layer", "default"),
        position=tuple(data.get("position", [0, 0, 0])),
    )
    register_node(node)
    if parent is not None:
        parent.add_child(node)
    for child_data in data.get("children", []):
        _build_node(child_data, parent=node)
    return node


def load_scene(filepath):
    """Load a scene graph from a JSON file. Returns the root node."""
    clear_registry()
    with open(filepath) as f:
        data = json.load(f)
    return _build_node(data)
