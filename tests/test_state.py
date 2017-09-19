import unittest

from exprail.grammar import Grammar
from exprail.state import State


class StateTest(unittest.TestCase):
    """Unittest for the State class"""

    def test_finish_states(self):
        grammar = Grammar('grammars/function.grammar')
        for node_id in [2, 12, 14, 18]:
            state = State(grammar, 'function', node_id, None)
            with self.assertRaises(RuntimeError):
                _ = state.find_successor_states()

    def test_unique_successor_states(self):
        grammar = Grammar('grammars/function.grammar')
        successors = {
            5: 2,
            6: 9,
            10: 8,
            11: 12,
            13: 14,
            15: 2,
            16: 17,
            17: 18
        }
        for source_id, target_id in successors.items():
            source = State(grammar, 'function', source_id)
            target = State(grammar, 'function', target_id)
            states = source.find_successor_states()
            self.assertEqual(states, {target})

    def test_multiple_successor_states(self):
        grammar = Grammar('grammars/function.grammar')
        successors = {
            1: [3, 11],
            3: [4, 13],
            4: [5, 8],
            8: [6, 7],
            9: [5, 10, 15]
        }
        for source_id, target_ids in successors.items():
            source = State(grammar, 'function', source_id)
            targets = {State(grammar, 'function', target_id) for target_id in target_ids}
            states = source.find_successor_states()
            self.assertEqual(states, targets)

    def test_recurrent_next_state(self):
        grammar = Grammar('grammars/function.grammar')
        token_state = State(grammar, 'skip', 3)
        finish_state = State(grammar, 'skip', 2)
        states = token_state.find_successor_states()
        self.assertEqual(states, {token_state, finish_state})

    def test_expression_entry(self):
        grammar = Grammar('grammars/function.grammar')
        source = State(grammar, 'function', 7)
        target = State(grammar, 'list', 5, State(grammar, 'function', 7))
        self.assertEqual(source.find_successor_states(), {target})

    def test_expression_exit(self):
        grammar = Grammar('grammars/function.grammar')
        source = State(grammar, 'list', 2, State(grammar, 'function', 7))
        target = State(grammar, 'function', 9)
        self.assertEqual(source.find_successor_states(), {target})
