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
    return available_states[0]


def collect_available_states(self, state):
    """
    Collect the available states from the current state.
    :param state: the current state of the parser
    :return: the list of the available states
    """
    return []
