import os
import unittest

from exprail.grammar import Grammar
from exprail.state import State
from exprail import router


class RouterTest(unittest.TestCase):
    """Unittest for routing in the grammar"""

    def setUp(self):
        if not os.path.isdir('/tmp/exprail'):
            raise RuntimeError('You should link the test grammar files into the /tmp directory!')

    def test_unique_available_state(self):
        grammar = Grammar('/tmp/exprail/function.grammar')
        connections = {
            5: 2,
            6: 9,
            7: 9,
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
            states = router.collect_available_states(source)
            self.assertEqual(states, {target})

    def test_recurrent_next_state(self):
        grammar = Grammar('/tmp/exprail/function.grammar')
        token_state = State(grammar, 'skip', 3)
        finish_state = State(grammar, 'skip', 2)
        states = router.collect_available_states(token_state)
        self.assertEqual(states, {token_state, finish_state})

    def test_multiple_next_states(self):
        grammar = Grammar('/tmp/exprail/function.grammar')
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
            states = router.collect_available_states(source)
            self.assertEqual(states, targets)

    def test_multiple_router_nodes(self):
        grammar = Grammar('/tmp/exprail/function.grammar')
        connections = {
            1: {3, 12},
            2: {2},
            3: {3},
            4: {4},
            5: {5},
            6: {6},
            8: {5, 6},
            9: {2, 5, 10},
            11: {12},
            13: {14},
            15: {2},
            16: {18},
            17: {18}
        }
        for source_id, node_ids in connections.items():
            start_state = State(grammar, 'function', source_id)
            router_states = router.find_router_states(start_state)
            result_node_ids = {state.node_id for state in router_states}
            self.assertEqual(result_node_ids, node_ids)
