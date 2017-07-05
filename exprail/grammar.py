"""
Grammar class definition
"""

from exprail.expression import Expression
from exprail.node import Node


class Grammar:
    """Represents a grammar"""

    def __init__(self, filename=None):
        self._expressions = {}
        if filename is not None:
            self.load_from_file(filename)
            self.validate()

    def load_from_file(self, filename):
        """Load the grammar from a grammar description."""
        with open(filename, 'r') as grammar_file:
            expression_name = ''
            for line in grammar_file:
                words = list(filter(None, line.split(' ')))
                if len(words) > 0:
                    if words[0] == 'expression':
                        expression_name = words[1][1:-2]
                        self._expressions[expression_name] = Expression()
                    elif len(words) == 5:
                        node_id = int(words[0])
                        node_type = words[1]
                        node_value = words[2][1:-1]
                        node = Node(node_type, node_value)
                        self._expressions[expression_name].add_node(node_id, node)
                    elif len(words) == 2:
                        source_id = int(words[0])
                        target_id = int(words[1])
                        self._expressions[expression_name].add_edge(source_id, target_id)

    def validate(self):
        """Validate the grammar."""
        # TODO: Raise errors when the grammar is invalid!
        pass

    def get_entry_node(self):
        """Get the entry node of the grammar."""
        pass
