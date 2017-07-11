"""
State class definition
"""


class State:
    """Represents the state of the parser."""

    def __init__(self, grammar, expression_name='', node_id=None):
        self._grammar = grammar
        if expression_name == '':
            if node_id is None:
                self.calc_initial_state()
            else:
                raise ValueError('Unnecessary node identifier argument!')
        elif expression_name in grammar.expressions:
            self._expression_name = expression_name
            if node_id in grammar[expression_name].nodes():
                self._node_id = node_id
            else:
                raise ValueError('The "{}" expression does not contain the node {}'.format(expression_name, node_id))
        else:
            raise ValueError('The grammar has no "{}" expression!'.format(expression_name))

    @property
    def expression_name(self):
        return self._expression_name

    @property
    def expression(self):
        return self._grammar[self._expression_name]

    @property
    def node_id(self):
        return self._node_id

    @property
    def node(self):
        return self.expression.nodes[self._node_id]

    def calc_initial_state(self):
        """Calculate the initial state of the given grammar."""
        self._expression_name = self._grammar.get_entry_expression_name()
        self._node_id = self._grammar.expressions[self._expression_name].get_start_node_id()
