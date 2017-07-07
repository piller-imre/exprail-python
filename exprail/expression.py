"""
Expression class definition
"""

from exprail.node import NodeType


class Expression:
    """Represents an expression as a syntax graph"""

    def __init__(self, index=None):
        self._nodes = {}
        self._index = index

    def is_entry_expression(self):
        """
        Signs that the expression is the entry expression of the grammar.
        :return: True, when the expression is an entry, else False
        """
        return self._index == 0

    def add_node(self, node_id, node):
        """Add new node to the expression."""
        self._nodes[node_id] = node

    def add_edge(self, source_id, target_id):
        """Add new edge to the expression."""
        source_node = self._nodes[source_id]
        target_node = self._nodes[target_id]
        source_node.add_target(target_node)

    def get_start_node(self):
        """
        Get the start node of the expression graph.
        :return: the start node
        """
        for node in self._nodes:
            if node.type is NodeType.START:
                return node
        raise RuntimeError('The start node is missing from the expression!')
