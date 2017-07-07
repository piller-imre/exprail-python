"""
Function for loading the grammar
"""

from exprail.expression import Expression
from exprail.node import Node


def load_expressions(path):
    """
    Load expressions from a grammar file.
    :param path: the path of the file
    :return: dictionary of expression objects
    """
    expressions = {}
    with open(path, 'r') as grammar_file:
        expression_name = ''
        for line in grammar_file:
            words = list(filter(None, line.split(' ')))
            if len(words) > 0:
                if words[0] == 'expression':
                    expression_name = words[1][1:-2]
                    expressions[expression_name] = Expression()
                elif len(words) == 5:
                    node_id = int(words[0])
                    node_type = words[1]
                    node_value = words[2][1:-1]
                    node = Node(node_type, node_value)
                    expressions[expression_name].add_node(node_id, node)
                elif len(words) == 2:
                    source_id = int(words[0])
                    target_id = int(words[1])
                    expressions[expression_name].add_edge(source_id, target_id)
    return expressions
