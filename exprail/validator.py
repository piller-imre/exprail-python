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
    n_start_nodes = 0
    for _, node in expression.nodes.items():
        if node.type is NodeType.START:
            n_start_nodes += 1
    if n_start_nodes < 1:
        raise RuntimeError('Missing start node!')
    elif n_start_nodes > 1:
        raise RuntimeError('Too many start nodes!')


def check_finish_node(expression):
    """
    Check that there is at least one finish node in the expression.
    :param expression: the validated expression object
    :return: None
    """
    for _, node in expression.nodes.items():
        if node.type is NodeType.FINISH:
            return
    raise RuntimeError('Missing finish node!')


def check_ground_nodes(expression):
    """
    Check that there is at most one ground node in the expression.
    :param expression: the validated expression object
    :return: None
    """
    n_ground_nodes = 0
    for _, node in expression.nodes.items():
        if node.type is NodeType.GROUND:
            n_ground_nodes += 1
    if n_ground_nodes > 1:
        raise RuntimeError('Too many ground nodes!')


def check_missing_node_values(expression):
    """
    Check that all necessary node value has given.
    :param expression: the validated expression object
    :return: None
    """
    require_node_value = {
        NodeType.EXPRESSION,
        NodeType.TOKEN,
        NodeType.EXCEPT_TOKEN,
        NodeType.ROUTER,
        NodeType.EXCEPT_ROUTER,
        NodeType.INFO,
        NodeType.ERROR,
        NodeType.OPERATION,
        NodeType.TRANSFORMATION
    }
    for _, node in expression.nodes.items():
        if node.type in require_node_value:
            if node.value == '':
                raise RuntimeError('Missing node value!')


def check_unnecessary_node_values(expression):
    """
    Check that there is no unnecessary node value where not necessary.
    :param expression: the validated expression object
    :return: None
    """
    do_not_require_node_values = {
        NodeType.START,
        NodeType.FINISH,
        NodeType.CONNECTION,
        NodeType.GROUND
    }
    for _, node in expression.nodes.items():
        if node.type in do_not_require_node_values:
            if node.value != '':
                raise RuntimeError('Unnecessary node value!')


def check_invalid_connections(expression):
    """
    Check the connections in the expression graph.
    :param expression: the validated expression object
    :return: None
    """
    for node_id, node in expression.nodes.items():
        n_source_nodes = len(expression.get_source_node_ids(node_id))
        if node.type in [NodeType.START, NodeType.GROUND]:
            if n_source_nodes > 0:
                raise RuntimeError('Invalid source for node {}!'.format(node_id))
        else:
            if n_source_nodes == 0:
                raise RuntimeError('Missing source for node {}!'.format(node_id))
        n_target_nodes = len(expression.get_target_node_ids(node_id))
        if node.type is NodeType.FINISH:
            if n_target_nodes > 0:
                raise RuntimeError('Invalid target for node {}!'.format(node_id))
        else:
            if n_target_nodes == 0:
                raise RuntimeError('Missing target for node {}!'.format(node_id))


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
    for expression in grammar.expressions.values():
        for node_id, node in expression.nodes.items():
            if node.type is NodeType.EXPRESSION:
                if node.value not in grammar.expressions:
                    raise RuntimeError('Invalid expression name "{}" at node {}!'.format(node.value, node_id))


def validate_grammar(grammar):
    """
    Validate the grammar.
    :param grammar: a grammar object
    :return: None
    """
    for _, expression in grammar.expressions.items():
        validate_expression(expression)
    check_referenced_expressions(grammar)
