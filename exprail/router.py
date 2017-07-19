"""
Functions for finding routes in the grammar.
"""

from exprail.state import State


def find_next_state(state, token):
    """
    Find the next state of the parser according to the current state and the token.
    :param state: the current state of the parser
    :param token: the currently processed token
    :return: the next state
    """
    available_states = collect_available_states(state)
    return None


def collect_available_states(state):
    """
    Collect the available states from the current state.
    :param state: the current state of the parser
    :return: the set of the available states
    """
    return set()


def find_router_node_ids(state):
    """
    Find the next available router nodes identifiers from the current node.
    The type of the router node is NodeType.ROUTER, NodeType.TOKEN and NodeType.FINISH.
    :param state: the start state of the searching
    :return: the set of router node identifiers
    """
    return set()
