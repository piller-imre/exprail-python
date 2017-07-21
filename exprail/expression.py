"""
Expression class definition
"""

from exprail.node import NodeType


class Expression:
    """Represents an expression as a syntax graph"""

    def __init__(self, index=None):
        self._nodes = {}
        self._edges = {}
        self._index = index

    @property
    def nodes(self):
        return self._nodes

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
        if source_id not in self._edges:
            self._edges[source_id] = set()
        self._edges[source_id].add(target_id)

    def get_start_node_id(self):
        """
        Get the identifier of the start node of the expression graph.
        :return: the identifier of the start node
        """
        for node_id, node in self._nodes.items():
            if node.type is NodeType.START:
                return node_id
        raise RuntimeError('The start node is missing from the expression!')

    def get_target_node_ids(self, node_id):
        """
        Get the identifiers of the target nodes from the given node.
        :param node_id: the identifier of the reference node
        :return: the set of target node identifiers
        :raises ValueError: when the node identifier is invalid
        """
        if node_id not in self._nodes:
            raise ValueError('The node id {} is invalid!'.format(node_id))
        if node_id not in self._edges:
            return set()
        return self._edges[node_id]
