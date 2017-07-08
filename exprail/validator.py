"""
Functions for validating the grammar.
"""

from exprail.node import NodeType


def check_start_node(expression):
    """
    Check that there is exactly one start node in the expression.
    :param expression: the validated expression object
    :return: None
    """
    pass


def check_finish_node(expression):
    """
    Check that there is exactly one finish node in the expression.
    :param expression: the validated expression object
    :return: None
    """
    pass


def check_ground_nodes(expression):
    """
    Check that there is at most one ground node in the expression.
    :param expression: the validated expression object
    :return: None
    """
    pass


def check_missing_node_values(expression):
    """
    Check that all necessary node value has given.
    :param expression: the validated expression object
    :return: None
    """
    pass


def check_unnecessary_node_values(expression):
    """
    Check that there is no unnecessary node value where not necessary.
    :param expression: the validated expression object
    :return: None
    """
    pass


def check_invalid_connections(expression):
    """
    Check the connections in the expression graph.
    :param expression: the validated expression object
    :return: None
    """
    pass


def validate_expression(expression):
    """
    Validate the given expression.
    :param expression: an expression object
    :return: None
    """
    check_start_node(expression)
    check_finish_node(expression)
    check_ground_nodes(expression)
    check_missing_node_values(expression)
    check_unnecessary_node_values(expression)
    check_invalid_connections(expression)


def check_referenced_expressions(grammar):
    """
    Check that all of the referenced expression name exists.
    :param grammar: a grammar object
    :return: None
    """
    pass


def validate_grammar(grammar):
    """
    Validate the grammar.
    :param grammar: a grammar object
    :return: None
    """
    for _, expression in grammar.expressions.items():
        validate_expression(expression)
    check_referenced_expressions(grammar)
