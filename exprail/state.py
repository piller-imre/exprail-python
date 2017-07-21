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
            expression = grammar.expressions[expression_name]
            if node_id is None:
                self._node_id = expression.get_start_node_id()
            else:
                if node_id in expression.nodes:
                    self._node_id = node_id
                else:
                    raise ValueError('The "{}" expression does not contain the node {}'.format(expression_name, node_id))
        else:
            raise ValueError('The grammar has no "{}" expression!'.format(expression_name))

    def __repr__(self):
        return '<State(expression_name=\'{}\', node_id={})>'.format(self._expression_name, self._node_id)

    def __eq__(self, other):
        # NOTE: It does not consider the grammar object!
        return self._expression_name == other.expression_name and self._node_id == other.node_id

    def __hash__(self):
        # NOTE: It does not consider the grammar object!
        return hash((self._expression_name, self._node_id))

    @property
    def grammar(self):
        return self._grammar

    @property
    def expression_name(self):
        return self._expression_name

    @property
    def expression(self):
        return self._grammar.expressions[self._expression_name]

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
