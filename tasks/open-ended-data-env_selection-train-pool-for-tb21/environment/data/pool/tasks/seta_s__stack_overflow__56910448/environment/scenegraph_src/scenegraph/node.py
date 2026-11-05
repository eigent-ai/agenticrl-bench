class SceneNode:
    """Represents a single node in a scene graph hierarchy."""

    def __init__(self, name, tag="Untagged", layer="default", position=(0, 0, 0)):
        self.name = name
        self.tag = tag
        self.layer = layer
        self.position = tuple(position)
        self.parent = None
        self.children = []
        self.handlers = {}

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def compare_tag(self, tag):
        """Case-insensitive tag comparison."""
        return self.tag.lower() == tag.lower()

    def add_handler(self, event_name, handler_info):
        self.handlers[event_name] = handler_info

    def __repr__(self):
        return f"SceneNode(name={self.name!r}, tag={self.tag!r}, layer={self.layer!r})"
