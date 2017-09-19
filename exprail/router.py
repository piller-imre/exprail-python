"""
Functions for finding routes in the grammar.
"""

from exprail.node import NodeType


def find_next_state(start_state, token):
    """
    Find the next state of the parser according to the current state and the token.
    :param start_state: the current state of the parser
    :param token: the currently processed token
    :return: the next state
    :raises RuntimeError: when the next state is missing or unambiguous
    """
    matching_states = set()
    default_states = set()
    for state in start_state.find_successor_states():
        if has_matching_successor(state, token):
            matching_states.add(state)
        if has_default_successor(state):
            default_states.add(state)
    if len(matching_states) == 1:
        return matching_states.pop()
    elif len(default_states) == 1:
        return default_states.pop()
    elif start_state.expression.has_ground_node():
        node_id = start_state.expression.get_ground_node_id()
        return start_state.at_node_id(node_id)
    else:
        raise RuntimeError('There is no possible next state!')


def has_matching_successor(state, token):
    """
    Check that is there any matching successor state.
    :param state: the start state of the searching
    :param token: the token which should be matched
    :return: True, when there is a matching successor, else False
    :raises RuntimeError: when there are multiple matching successors
    """
    classifier = state.grammar.classifier
    n_matching_successors = 0
    for successor in collect_matchable_successors(state):
        if successor.node.type in [NodeType.ROUTER, NodeType.TOKEN]:
            if classifier.is_in_class(successor.node.value, token):
                n_matching_successors += 1
        elif successor.node.type in [NodeType.EXCEPT_ROUTER, NodeType.EXCEPT_TOKEN]:
            if not classifier.is_in_class(successor.node.value, token):
                n_matching_successors += 1
    if n_matching_successors == 0:
        return False
    elif n_matching_successors == 1:
        return True
    else:
        raise RuntimeError('There are multiple matching successors!')


def has_default_successor(start_state):
    """
    Check that is there any default successor state.
    NOTE: The start state also evaluated as a successor!
    :param start_state: the start state of the searching
    :return: True, when there is a default successor, else False
    """
    processable_states = {start_state}
    visited_states = set()
    while processable_states:
        state = processable_states.pop()
        if state not in visited_states:
            if state.node.is_default():
                return True
            elif not state.node.is_matchable():
                processable_states.update(state.find_successor_states())
            visited_states.add(state)
    return False


def collect_matchable_successors(start_state):
    """
    Collect the matchable successor states.
    NOTE: The start state also evaluated as a successor!
    :param start_state: the start state of the searching
    :return: the set of matchable successors
    """
    processable_states = {start_state}
    matchable_states = set()
    visited_states = set()
    while processable_states:
        state = processable_states.pop()
        if state not in visited_states:
            if state.node.is_matchable():
                matchable_states.add(state)
            elif not state.node.is_default():
                processable_states.update(state.find_successor_states())
            visited_states.add(state)
    return matchable_states


def collect_default_successors(start_state):
    """
    Collect the default successor states.
    NOTE: The start state also evaluated as a successor!
    NOTE: This function is necessary for expression validation!
    :param start_state: the start state of the searching
    :return: the set of default successor states
    """
    processable_states = {start_state}
    default_states = set()
    visited_states = set()
    while processable_states:
        state = processable_states.pop()
        if state not in visited_states:
            if state.node.is_default():
                default_states.add(state)
            elif not state.node.is_matchable():
                processable_states.update(state.find_successor_states())
            visited_states.add(state)
    return default_states
