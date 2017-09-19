import unittest

from exprail.classifier import Classifier
from exprail.grammar import Grammar
from exprail.state import State
from exprail.token import Token
from exprail import router


class FunctionClassifier(Classifier):
    """Classifier for the function grammar"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Classify the parametrization of a function call.
        :param token_class: 'keyword', 'number', 'comma', '(', ')', '[', ']', 'whitespace'
        :param token: the processed token
        :return: True, when the token is in the class, else False
        """
        return token_class == token.type


class RouterTest(unittest.TestCase):
    """Unittest for routing in the grammar"""

    def test_find_next_state(self):
        grammar = Grammar('grammars/function.grammar', classifier=FunctionClassifier())
        transitions = [
            {
                'source': State(grammar, 'function', 1),
                'token': Token('keyword', ''),
                'target': State(grammar, 'function', 3)
            },
            {
                'source': State(grammar, 'function', 1),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 11)
            },
            {
                'source': State(grammar, 'function', 2),
                'token': Token('keyword', ''),
                'target': None
            },
            {
                'source': State(grammar, 'function', 3),
                'token': Token('(', ''),
                'target': State(grammar, 'function', 4)
            },
            {
                'source': State(grammar, 'function', 3),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 13)
            },
            {
                'source': State(grammar, 'function', 4),
                'token': Token(')', ''),
                'target': State(grammar, 'function', 5)
            },
            {
                'source': State(grammar, 'function', 4),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 8)
            },
            {
                'source': State(grammar, 'function', 4),
                'token': Token('[', ''),
                'target': State(grammar, 'list', 8)
            },
            {
                'source': State(grammar, 'function', 4),
                'token': Token('keyword', ''),
                'target': State(grammar, 'function', 16)
            },
            {
                'source': State(grammar, 'function', 5),
                'token': Token('empty', ''),
                'target': State(grammar, 'function', 2)
            },
            {
                'source': State(grammar, 'function', 6),
                'token': Token(')', ''),
                'target': State(grammar, 'function', 9)
            },
            {
                'source': State(grammar, 'function', 6),
                'token': Token('comma', ''),
                'target': State(grammar, 'function', 9)
            },
            {
                'source': State(grammar, 'function', 6),
                'token': Token('empty', ''),
                'target': State(grammar, 'function', 9)
            },
            {
                'source': State(grammar, 'function', 7),
                'token': Token('[', ''),
                'target': State(grammar, 'list', 5, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'function', 7),
                'token': Token('keyword', ''),
                'target': State(grammar, 'list', 8, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'function', 8),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 6)
            },
            {
                'source': State(grammar, 'function', 8),
                'token': Token('[', ''),
                'target': State(grammar, 'function', 7)
            },
            {
                'source': State(grammar, 'function', 8),
                'token': Token('keyword', ''),
                'target': State(grammar, 'function', 16)
            },
            {
                'source': State(grammar, 'function', 9),
                'token': Token(')', ''),
                'target': State(grammar, 'function', 5)
            },
            {
                'source': State(grammar, 'function', 9),
                'token': Token('comma', ''),
                'target': State(grammar, 'function', 10)
            },
            {
                'source': State(grammar, 'function', 9),
                'token': Token('keyword', ''),
                'target': State(grammar, 'function', 15)
            },
            {
                'source': State(grammar, 'function', 10),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 8)
            },
            {
                'source': State(grammar, 'function', 10),
                'token': Token('[', ''),
                'target': State(grammar, 'function', 8)
            },
            {
                'source': State(grammar, 'function', 10),
                'token': Token('keyword', ''),
                'target': State(grammar, 'function', 16)
            },
            {
                'source': State(grammar, 'function', 11),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 12)
            },
            {
                'source': State(grammar, 'function', 12),
                'token': Token('number', ''),
                'target': None
            },
            {
                'source': State(grammar, 'function', 13),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 14)
            },
            {
                'source': State(grammar, 'function', 14),
                'token': Token('number', ''),
                'target': None
            },
            {
                'source': State(grammar, 'function', 15),
                'token': Token('keyword', ''),
                'target': State(grammar, 'function', 2)
            },
            {
                'source': State(grammar, 'function', 16),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 17)
            },
            {
                'source': State(grammar, 'function', 17),
                'token': Token('number', ''),
                'target': State(grammar, 'function', 18)
            },
            {
                'source': State(grammar, 'function', 18),
                'token': Token('number', ''),
                'target': None
            },
            {
                'source': State(grammar, 'list', 1, State(grammar, 'function', 7)),
                'token': Token('[', ''),
                'target': State(grammar, 'list', 5, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 1, State(grammar, 'function', 7)),
                'token': Token('number', ''),
                'target': State(grammar, 'list', 8, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 2, State(grammar, 'function', 7)),
                'token': Token(')', ''),
                'target': State(grammar, 'function', 9)
            },
            {
                'source': State(grammar, 'list', 2, State(grammar, 'function', 7)),
                'token': Token('comma', ''),
                'target': State(grammar, 'function', 9)
            },
            {
                'source': State(grammar, 'list', 2, State(grammar, 'function', 7)),
                'token': Token('keyword', ''),
                'target': State(grammar, 'function', 9)
            },
            {
                'source': State(grammar, 'list', 3, State(grammar, 'function', 7)),
                'token': Token('number', ''),
                'target': State(grammar, 'list', 4, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 3, State(grammar, 'function', 7)),
                'token': Token('keyword', ''),
                'target': State(grammar, 'list', 8, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 4, State(grammar, 'function', 7)),
                'token': Token(']', ''),
                'target': State(grammar, 'list', 6, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 4, State(grammar, 'function', 7)),
                'token': Token('comma', ''),
                'target': State(grammar, 'list', 8, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 5, State(grammar, 'function', 7)),
                'token': Token(']', ''),
                'target': State(grammar, 'list', 7, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 5, State(grammar, 'function', 7)),
                'token': Token('number', ''),
                'target': State(grammar, 'list', 4, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 5, State(grammar, 'function', 7)),
                'token': Token('keyword', ''),
                'target': State(grammar, 'list', 8, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 6, State(grammar, 'function', 7)),
                'token': Token(')', ''),
                'target': State(grammar, 'list', 2, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 6, State(grammar, 'function', 7)),
                'token': Token('comma', ''),
                'target': State(grammar, 'list', 2, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 6, State(grammar, 'function', 7)),
                'token': Token('keyword', ''),
                'target': State(grammar, 'list', 2, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 7, State(grammar, 'function', 7)),
                'token': Token(']', ''),
                'target': State(grammar, 'list', 6, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 7, State(grammar, 'function', 7)),
                'token': Token('comma', ''),
                'target': State(grammar, 'list', 8, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 8, State(grammar, 'function', 7)),
                'token': Token('comma', ''),
                'target': State(grammar, 'list', 9, State(grammar, 'function', 7))
            },
            {
                'source': State(grammar, 'list', 9, State(grammar, 'function', 7)),
                'token': Token('comma', ''),
                'target': State(grammar, 'list', 10, State(grammar, 'function', 7))
            }
        ]
        for transition in transitions:
            target_state = transition['target']
            if target_state is not None:
                self.assertEqual(router.find_next_state(transition['source'], transition['token']), target_state)
            else:
                with self.assertRaises(RuntimeError):
                    router.find_next_state(transition['source'], transition['token'])
