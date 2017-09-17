"""
Functions for finding routes in the grammar.
"""

from exprail.state import State
from exprail.node import NodeType


def find_next_state(state, token):
    """
    Find the next state of the parser according to the current state and the token.
    :param state: the current state of the parser
    :param token: the currently processed token
    :return: the next state
    :raises RuntimeError: when the next state is missing or unambiguous
    """
    matching_states, default_states = collect_possible_next_states(state, token)
    next_state = choose_next_state(matching_states, default_states)
    if next_state is None:
        # TODO: Use the ground node as a default case!
        pass
    return next_state


def collect_possible_next_states(start_state, token):
    """
    Collect the possible next states from the available states.
    :param start_state: the current state of the parser
    :param token: the processed token
    :return: the sets of matching and default states
    """
    # TODO: Apply the transformation node!
    classifier = start_state.grammar.classifier
    matching_states = set()
    default_states = set()
    for available_state in collect_available_states(start_state):
        for state in find_router_states(available_state):
            if state.node.type in [NodeType.ROUTER, NodeType.TOKEN]:
                if classifier.is_in_class(state.node.value, token):
                    matching_states.add(available_state)
            elif state.node.type in [NodeType.EXCEPT_ROUTER, NodeType.EXCEPT_TOKEN]:
                if not classifier.is_in_class(state.node.value, token):
                    matching_states.add(available_state)
            elif state.node.type in [NodeType.DEFAULT_ROUTER, NodeType.DEFAULT_TOKEN, NodeType.FINISH]:
                default_states.add(available_state)
    return matching_states, default_states


def choose_next_state(matching_states, default_states):
    """
    Choose the next state from the matching and finish states
    NOTE: The None as the return value is necessary for the ground node!
    :param matching_states: the set of states which matches with the current token
    :param default_states: the set of available default cases
    :return: the next state when available or None when there is no match
    :raises RuntimeError: when the next state is unambiguous
    """
    if len(default_states) > 1:
        raise RuntimeError('There are too many default cases!')
    if len(matching_states) == 1:
        next_state = matching_states.pop()
        return next_state
    elif len(matching_states) == 0:
        if len(default_states) == 1:
            next_state = default_states.pop()
            return next_state
        elif len(default_states) == 0:
            return None
    else:
        raise RuntimeError('There are too many matching states!')


def collect_available_states(state):
    """
    Collect the available states from the current state.
    :param state: the current state of the parser
    :return: the set of the available states
    """
    target_node_ids = state.expression.get_target_node_ids(state.node_id)
    available_states = {state.at_node_id(node_id) for node_id in target_node_ids}
    return available_states


def find_router_states(start_state):
    """
    Find the available router states from the current state.
    The type of the router node can be on of the followings:
    - NodeType.ROUTER,
    - NodeType.EXCEPT_ROUTER,
    - NodeType.DEFAULT_ROUTER,
    - NodeType.TOKEN,
    - NodeType.EXCEPT_TOKEN,
    - NodeType.DEFAULT_TOKEN,
    - NodeType.FINISH.
    The router node is the current node of the state when the type matches.
    :param start_state: the start state of the searching
    :return: set of router states
    """
    router_states = set()
    visited_states = set()
    next_states = {start_state}
    while next_states:
        state = next_states.pop()
        if state not in visited_states:
            visited_states.add(state)
            if state.node.type is NodeType.EXPRESSION:
                expression_name = state.node.value
                node_id = state.grammar.expressions[expression_name].get_start_node_id()
                entry_state = State(state.grammar, expression_name, node_id, state)
                next_states.add(entry_state)
            elif state.node.type is NodeType.FINISH:
                router_states.add(state.return_state or state)
            elif state.node.has_routing_information():
                router_states.add(state)
            else:
                for node_id in state.expression.get_target_node_ids(state.node_id):
                    next_state = state.at_node_id(node_id)
                    next_states.add(next_state)
    return router_states
