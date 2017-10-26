import os
import unittest

from exprail import loader
from exprail.node import NodeType


class LoaderTest(unittest.TestCase):
    """Unittest for grammar loading"""

    def test_missing_grammar_file(self):
        with self.assertRaises(ValueError):
            _ = loader.load_expressions('grammars/missing.grammar')

    def test_empty_grammar_file(self):
        expressions = loader.load_expressions('grammars/empty.grammar')
        self.assertEqual(len(expressions), 0)

    def test_single_expression(self):
        expressions = loader.load_expressions('grammars/single.grammar')
        self.assertEqual(len(expressions), 1)
        self.assertIn('sample', expressions)
        expression = expressions['sample']
        self.assertTrue(expression.is_entry_expression())
        nodes = expression.nodes
        self.assertEqual(len(nodes), 4)
        self.assertIn(1, nodes)
        self.assertEqual(nodes[1].type, NodeType.START)
        self.assertEqual(nodes[1].value, '')
        self.assertIn(2, nodes)
        self.assertEqual(nodes[2].type, NodeType.INFO)
        self.assertEqual(nodes[2].value, 'Nothing new')
        self.assertIn(3, nodes)
        self.assertEqual(nodes[3].type, NodeType.EXPRESSION)
        self.assertEqual(nodes[3].value, 'sample')
        self.assertIn(4, nodes)
        self.assertEqual(nodes[4].type, NodeType.FINISH)
        self.assertEqual(nodes[4].value, '')
        targets = {
            1: {2},
            2: {3},
            3: {4},
            4: set()
        }
        for node_id, reference_ids in targets.items():
            target_ids = expression.get_target_node_ids(node_id)
            self.assertEqual(target_ids, reference_ids)

    def test_escaped_characters(self):
        expressions = loader.load_expressions('grammars/escaped_names.grammar')
        self.assertEqual(len(expressions), 1)
        self.assertIn('escaped', expressions)
        expression = expressions['escaped']
        self.assertEqual(len(expression.nodes), 7)
        self.assertEqual(expression.nodes[2].value, 'a \" character')
        self.assertEqual(expression.nodes[3].value, 'a \\ character')
        self.assertEqual(expression.nodes[4].value, 'both \" and \\ characters')
        self.assertEqual(expression.nodes[5].value, 'multiple \"\\\" and \\\\\" in value')
        self.assertEqual(expression.nodes[6].value, 'three   two  one zero')

    def test_empty_expressions(self):
        expressions = loader.load_expressions('grammars/empties.grammar')
        self.assertEqual(len(expressions), 6)
        expression_names = [
            'first',
            'the second',
            'some more words in expression name',
            'name with \" character',
            'name with \\ character',
            'both \\\" and \"\\ character combinations'
        ]
        for name, expression in expressions.items():
            self.assertIn(name, expression_names)
            self.assertEqual(len(expression.nodes), 0)

    def test_multiple_expressions(self):
        expressions = loader.load_expressions('grammars/multiple.grammar')
        self.assertEqual(len(expressions), 2)
        self.assertIn('first', expressions)
        expression = expressions['first']
        self.assertEqual(len(expression.nodes), 6)
        self.assertIn('second', expressions)
        targets = {
            1: {4, 5},
            2: set(),
            3: {2},
            4: {3, 6},
            5: {6},
            6: {2}
        }
        for node_id, reference_ids in targets.items():
            target_ids = expression.get_target_node_ids(node_id)
            self.assertEqual(target_ids, reference_ids)
        expression = expressions['second']
        self.assertEqual(len(expression.nodes), 5)
        targets = {
            1: {3, 4, 5},
            2: set(),
            3: {2},
            4: {2},
            5: {2}
        }
        for node_id, reference_ids in targets.items():
            target_ids = expression.get_target_node_ids(node_id)
            self.assertEqual(target_ids, reference_ids)
