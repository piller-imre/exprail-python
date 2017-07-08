"""
Function for loading the grammar
"""

import os

from exprail.expression import Expression
from exprail.node import Node


def get_string_content(line):
    """
    Get the quoted string content from a line.
    :param line: a string which contains a quoted substring
    :return: the string between the quotes
    """
    first_index = line.find('\"') + 1
    last_index = line.rfind('\"')
    content = line[first_index:last_index]
    content = content.replace('\\\"', '\"')
    content = content.replace('\\\\', '\\')
    return content


def load_expressions(path):
    """
    Load expressions from a grammar file.
    :param path: the path of the file
    :return: dictionary of expression objects
    """
    expressions = {}
    expression_index = 0
    if not os.path.isfile(path):
        raise ValueError('Invalid grammar file path "{}"!'.format(path))
    with open(path, 'r') as grammar_file:
        expression_name = ''
        for line in grammar_file:
            words = list(filter(None, line.split(' ')))
            if len(words) > 0:
                if words[0] == 'expression':
                    expression_name = get_string_content(line)
                    expressions[expression_name] = Expression(expression_index)
                    expression_index += 1
                elif len(words) >= 5:
                    node_id = int(words[0])
                    node_type = words[1]
                    node_value = get_string_content(line)
                    node = Node(node_type, node_value)
                    expressions[expression_name].add_node(node_id, node)
                elif len(words) == 2:
                    source_id = int(words[0])
                    target_id = int(words[1])
                    expressions[expression_name].add_edge(source_id, target_id)
    return expressions
