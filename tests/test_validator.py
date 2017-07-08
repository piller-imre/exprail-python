import unittest

from exprail.expression import Expression
from exprail.grammar import Grammar
from exprail.node import Node
from exprail.node import NodeType
from exprail import validator


class ValidatorTest(unittest.TestCase):
    """Unittest for grammar validation"""

    def test_missing_start_node(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.INFO, 'validation test'))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_edge(1, 2)
        with self.assertRaises(RuntimeError):
            validator.check_start_node(expression)

    def test_multiple_start_node(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.START))
        expression.add_node(3, Node(NodeType.INFO, 'validation test'))
        expression.add_node(4, Node(NodeType.FINISH))
        expression.add_edge(1, 3)
        expression.add_edge(2, 3)
        expression.add_edge(3, 4)
        with self.assertRaises(RuntimeError):
            validator.check_start_node(expression)

    def test_missing_finish_node(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.INFO, 'validation test'))
        expression.add_edge(1, 2)
        with self.assertRaises(RuntimeError):
            validator.check_finish_node(expression)

    def test_multiple_finish_node(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.INFO, 'validation test'))
        expression.add_node(3, Node(NodeType.FINISH))
        expression.add_node(4, Node(NodeType.FINISH))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        expression.add_edge(2, 4)
        with self.assertRaises(RuntimeError):
            validator.check_finish_node(expression)

    def test_multiple_ground_nodes(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.GROUND))
        expression.add_node(4, Node(NodeType.GROUND))
        expression.add_edge(1, 2)
        with self.assertRaises(RuntimeError):
            validator.check_ground_nodes(expression)

    def test_missing_expression_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.EXPRESSION))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_missing_node_values(expression)

    def test_missing_info_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.INFO))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_missing_node_values(expression)

    def test_missing_error_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.ERROR))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_missing_node_values(expression)

    def test_missing_transformation_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.TRANSFORMATION))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_missing_node_values(expression)

    def test_missing_operation_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.OPERATION))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_missing_node_values(expression)

    def test_missing_router_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.ROUTER))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_missing_node_values(expression)

    def test_missing_token_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.TOKEN))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_missing_node_values(expression)

    def test_unnecessary_start_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START, 'start'))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_edge(1, 2)
        with self.assertRaises(RuntimeError):
            validator.check_unnecessary_node_values(expression)

    def test_unnecessary_finish_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH, 'finish'))
        expression.add_edge(1, 2)
        with self.assertRaises(RuntimeError):
            validator.check_unnecessary_node_values(expression)

    def test_unnecessary_connection_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.CONNECTION, 'connection'))
        expression.add_node(3, Node(NodeType.FINISH))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_unnecessary_node_values(expression)

    def test_unnecessary_ground_node_value(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.GROUND, 'ground'))
        expression.add_edge(1, 2)
        with self.assertRaises(RuntimeError):
            validator.check_unnecessary_node_values(expression)

    def test_missing_start_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.GROUND))
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_invalid_start_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.GROUND))
        expression.add_edge(1, 2)
        expression.add_edge(3, 1)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_finish_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.ERROR, 'error'))
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_invalid_finish_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.GROUND))
        expression.add_edge(1, 2)
        expression.add_edge(2, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_connection_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.CONNECTION))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_connection_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.CONNECTION))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_expression_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.EXPRESSION, 'expression'))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_expression_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.EXPRESSION, 'expression'))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_info_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.INFO, 'info'))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_info_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.INFO, 'info'))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_error_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.ERROR, 'error'))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_error_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.ERROR, 'error'))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_transformation_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.TRANSFORMATION, 'transformation'))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_transformation_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.TRANSFORMATION, 'transformation'))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_operation_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.OPERATION, 'operation'))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_operation_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.OPERATION, 'operation'))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_stack_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.STACK))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_stack_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.STACK))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_clean_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.CLEAN))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_clean_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.CLEAN))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_invalid_ground_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.GROUND))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_ground_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.GROUND))
        expression.add_edge(1, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_router_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.ROUTER, 'router'))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_router_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.ROUTER, 'router'))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_token_node_source(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.TOKEN, 'token'))
        expression.add_edge(1, 2)
        expression.add_edge(3, 2)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_missing_token_node_target(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.TOKEN, 'token'))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        with self.assertRaises(RuntimeError):
            validator.check_invalid_connections(expression)

    def test_referenced_expressions(self):
        expression = Expression()
        expression.add_node(1, Node(NodeType.START))
        expression.add_node(2, Node(NodeType.FINISH))
        expression.add_node(3, Node(NodeType.EXPRESSION, 'expression'))
        expression.add_edge(1, 2)
        expression.add_edge(1, 3)
        expression.add_edge(3, 2)
        grammar = Grammar()
        grammar.add_expression('sample', expression)
        with self.assertRaises(RuntimeError):
            validator.check_referenced_expressions(grammar)
