def get_root_tag(node):
    """Return the tag of the root node in this node's hierarchy."""
    if node.parent is not None:
        return node.parent.tag
    return node.tag


def get_ancestor_chain(node):
    """Return the list of ancestors from immediate parent up to the root."""
    chain = [node]
    current = node.parent
    while current is not None:
        chain.append(current)
        current = current.parent
    return chain
