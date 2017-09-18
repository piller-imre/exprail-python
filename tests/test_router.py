import os
import unittest

from exprail.grammar import Grammar
from exprail.state import State
from exprail import router


class RouterTest(unittest.TestCase):
    """Unittest for routing in the grammar"""

    def test_unique_successor_state(self):
        grammar = Grammar('grammars/function.grammar')
        connections = {
            5: 2,
            6: 9,
            10: 8,
            11: 12,
            13: 14,
            15: 2,
            16: 17,
            17: 18
        }
        for source_id, target_id in connections.items():
            source = State(grammar, 'function', source_id)
            target = State(grammar, 'function', target_id)
            states = source.find_successor_states()
            self.assertEqual(states, {target})

    def test_recurrent_next_state(self):
        grammar = Grammar('grammars/function.grammar')
        token_state = State(grammar, 'skip', 3)
        finish_state = State(grammar, 'skip', 2)
        states = token_state.find_successor_states()
        self.assertEqual(states, {token_state, finish_state})

    def test_multiple_next_states(self):
        grammar = Grammar('grammars/function.grammar')
        connections = {
            1: [3, 11],
            3: [4, 13],
            4: [5, 8],
            8: [6, 7],
            9: [5, 10, 15]
        }
        for source_id, target_ids in connections.items():
            source = State(grammar, 'function', source_id)
            targets = {State(grammar, 'function', target_id) for target_id in target_ids}
            states = source.find_successor_states()
            self.assertEqual(states, targets)

    def test_multiple_matchable_states(self):
        grammar = Grammar('grammars/function.grammar')
        connections = {
            1: {3},
            2: set(),
            3: {3},
            4: {4},
            5: {5},
            6: {6},
            7: {5},
            8: {5, 6},
            9: {5, 10},
            10: {10},
            11: set(),
            12: set(),
            13: set(),
            14: set(),
            15: set(),
            16: set(),
            17: set(),
            18: set()
        }
        for source_id, node_ids in connections.items():
            start_state = State(grammar, 'function', source_id)
            router_states = router.collect_matchable_successors(start_state)
            result_node_ids = {state.node_id for state in router_states}
            self.assertEqual(result_node_ids, node_ids)
