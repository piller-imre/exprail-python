"""
State class definition
"""


class State:
    """Represents the state of the parser."""

    def __init__(self, grammar, expression_name, node_id, return_state=None):
        if expression_name not in grammar.expressions:
            raise ValueError('The grammar has no "{}" expression!'.format(expression_name))
        if node_id not in grammar.expressions[expression_name].nodes:
            raise ValueError('The "{}" expression does not contain the node {}'.format(expression_name, node_id))
        self._grammar = grammar
        self._expression_name = expression_name
        self._node_id = node_id
        self._return_state = return_state

    def __repr__(self):
        if self._return_state is None:
            return '<State(expression_name=\'{}\', node_id={})>'.format(self._expression_name, self._node_id)
        else:
            args = (self._expression_name, self._node_id, self._return_state)
            return '<State(expression_name=\'{}\', node_id={}, return_state={})>'.format(*args)

    def __eq__(self, other):
        # NOTE: It does not consider the grammar object!
        conditions = [
            self._expression_name == other.expression_name,
            self._node_id == other.node_id,
            self._return_state == other.return_state
        ]
        return all(conditions)

    def __hash__(self):
        # NOTE: It does not consider the grammar object!
        return hash((self._expression_name, self._node_id, self._return_state))

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

    @property
    def return_state(self):
        return self._return_state

    def at_node_id(self, node_id):
        """
        Returns with a new state with different node identifier then the current.
        :param node_id: an other node identifier of the expression
        :return: a state object
        """
        return State(self._grammar, self._expression_name, node_id, self._return_state)
