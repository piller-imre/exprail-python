"""
State class definition
"""


class State:
    """Represents the state of the parser."""

    def __init__(self, grammar, expression_name='', node_id=None):
        self._grammar = grammar
        self._expression_name = expression_name
        self._node_id = node_id
        if expression_name == '' and node_id is None:
            self.calc_initial_state()

    @property
    def node(self):
        return self._grammar.expressions[self._expression_name].nodes[self._node_id]

    def calc_initial_state(self):
        """Calculate the initial state of the given grammar."""
        self._expression_name = self._grammar.get_entry_expression_name()
        self._node_id = self._grammar.expressions[self._expression_name].get_start_node_id()
