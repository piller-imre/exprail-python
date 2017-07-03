"""
Expression class definition
"""


class Expression:
    """Represents an expression as a syntax graph"""

    def __init__(self):
        self._nodes = {}

    def add_node(self, node_id, node):
        """Add new node to the expression."""
        self._nodes[node_id] = node

    def add_edge(self, source_id, target_id):
        """Add new edge to the expression."""
        source_node = self._nodes[source_id]
        target_node = self._nodes[target_id]
        source_node.add_target(target_node)
