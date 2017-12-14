"""
State class definition
"""

from exprail.node import NodeType


class State(object):
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

    def find_successor_states(self):
        """
        Find the successor states of the given state.
        :return: the set of successor states
        """
        if self.node.type is NodeType.EXPRESSION:
            expression_name = self.node.value
            node_id = self._grammar.expressions[expression_name].get_start_node_id()
            start_state = State(self._grammar, expression_name, node_id, self)
            return start_state.find_successor_states()
        elif self.node.type is NodeType.FINISH:
            if self._return_state is not None:
                target_node_ids = self.return_state.expression.get_target_node_ids(self.return_state.node_id)
                successor_states = {self.return_state.at_node_id(node_id) for node_id in target_node_ids}
                return successor_states
            else:
                raise RuntimeError('The top level expression finish nodes have no successors!')
        else:
            target_node_ids = self.expression.get_target_node_ids(self.node_id)
            successor_states = {self.at_node_id(node_id) for node_id in target_node_ids}
            return successor_states
