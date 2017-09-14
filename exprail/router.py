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


def collect_possible_next_states(state, token):
    """
    Collect the possible next states from the available states.
    :param state: the current state of the parser
    :param token: the processed token
    :return: the sets of matching and default states
    """
    # TODO: Apply the transformation node!
    classifier = state.grammar.classifier
    matching_states = set()
    default_states = set()
    available_states = collect_available_states(state)
    router_node_types = [
        NodeType.ROUTER,
        NodeType.EXCEPT_ROUTER,
        NodeType.DEFAULT_ROUTER,
        NodeType.TOKEN,
        NodeType.EXCEPT_TOKEN,
        NodeType.DEFAULT_TOKEN,
        NodeType.FINISH
    ]
    for available_state in available_states:
        router_nodes = find_router_nodes(available_state)
        for node in router_nodes:
            assert node.type in router_node_types
            if node.type in [NodeType.ROUTER, NodeType.TOKEN]:
                if classifier.is_in_class(node.value, token):
                    matching_states.add(available_state)
            elif node.type in [NodeType.EXCEPT_ROUTER, NodeType.EXCEPT_TOKEN]:
                if not classifier.is_in_class(node.value, token):
                    matching_states.add(available_state)
            elif node.type in [NodeType.DEFAULT_ROUTER, NodeType.DEFAULT_TOKEN, NodeType.FINISH]:
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
    available_states = {State(state.grammar, state.expression_name, node_id) for node_id in target_node_ids}
    return available_states


def find_router_nodes(state):
    """
    Find the available router node identifiers from the current node.
    The type of the router node can be on of the followings:
    - NodeType.ROUTER,
    - NodeType.EXCEPT_ROUTER,
    - NodeType.DEFAULT_ROUTER,
    - NodeType.TOKEN,
    - NodeType.EXCEPT_TOKEN,
    - NodeType.DEFAULT_TOKEN,
    - NodeType.FINISH.
    The router node is the current node of the state when the type matches.
    :param state: the start state of the searching
    :return: set of router nodes
    """
    # TODO: Search nodes over expression type nodes!
    router_nodes = set()
    visited_node_ids = set()
    next_node_ids = {state.node_id}
    router_node_types = [
        NodeType.ROUTER,
        NodeType.EXCEPT_ROUTER,
        NodeType.DEFAULT_ROUTER,
        NodeType.TOKEN,
        NodeType.EXCEPT_TOKEN,
        NodeType.DEFAULT_TOKEN,
        NodeType.FINISH
    ]
    while next_node_ids:
        node_id = next_node_ids.pop()
        if node_id not in visited_node_ids:
            visited_node_ids.add(node_id)
            node = state.expression.nodes[node_id]
            if node.type in router_node_types:
                router_nodes.add(node)
            else:
                next_node_ids.update(state.expression.get_target_node_ids(node_id))
    return router_nodes
