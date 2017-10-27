import unittest

from exprail.classifier import Classifier
from exprail.grammar import Grammar
from exprail.parser import Parser
from exprail.source import SourceString


class WsClassifier(Classifier):
    """Classify alphabetic characters and whitespaces"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Distinguish alphabetic characters and whitespaces.
        :param token_class: 'a-Z' or 'ws' set names
        :param token: the value of the token
        :return: True, when the token is in the class, else False
        """
        if token.type == 'empty':
            return False
        if token_class == 'ws':
            return token.value == ' '
        else:
            return token.value != ' '


class WsParser(Parser):
    """Parse the input text and print the words"""

    def __init__(self, grammar, source):
        super(WsParser, self).__init__(grammar, source)
        self._result = []

    @property
    def result(self):
        return self._result

    def operate(self, operation, token):
        """Print the token value on print operation."""
        if operation == 'save':
            word = ''.join(self._stacks[''])
            self._result.append(word)
        else:
            raise ValueError('The "{}" is an invalid operation!'.format(operation))


class WordsGrammarTest(unittest.TestCase):
    """Words grammar tests with examples"""

    def test_empty_source(self):
        ws_classifier = WsClassifier()
        grammar = Grammar(filename='grammars/words.grammar', classifier=ws_classifier)
        source = SourceString(r'')
        parser = WsParser(grammar, source)
        parser.parse()
        self.assertEqual(parser.result, [])

    def test_single_word(self):
        ws_classifier = WsClassifier()
        grammar = Grammar(filename='grammars/words.grammar', classifier=ws_classifier)
        source = SourceString(r'single')
        parser = WsParser(grammar, source)
        parser.parse()
        self.assertEqual(parser.result, ['single'])

    def test_multiple_words(self):
        ws_classifier = WsClassifier()
        grammar = Grammar(filename='grammars/words.grammar', classifier=ws_classifier)
        source = SourceString(r'Some simple words after each others')
        parser = WsParser(grammar, source)
        parser.parse()
        words = [
            'Some', 'simple', 'words', 'after', 'each', 'others'
        ]
        self.assertEqual(parser.result, words)

    def test_only_spaces(self):
        ws_classifier = WsClassifier()
        grammar = Grammar(filename='grammars/words.grammar', classifier=ws_classifier)
        source = SourceString(r'    ')
        parser = WsParser(grammar, source)
        parser.parse()
        self.assertEqual(parser.result, [])

    def test_multiple_separator_spaces(self):
        ws_classifier = WsClassifier()
        grammar = Grammar(filename='grammars/words.grammar', classifier=ws_classifier)
        source = SourceString(r'Some  simple words    after  each  others')
        parser = WsParser(grammar, source)
        parser.parse()
        words = [
            'Some', 'simple', 'words', 'after', 'each', 'others'
        ]
        self.assertEqual(parser.result, words)

    def test_leading_and_trailing_spaces(self):
        ws_classifier = WsClassifier()
        grammar = Grammar(filename='grammars/words.grammar', classifier=ws_classifier)
        source = SourceString(r'   Leading  and  trailing spaces   ')
        parser = WsParser(grammar, source)
        parser.parse()
        words = [
            'Leading', 'and', 'trailing', 'spaces'
        ]
        self.assertEqual(parser.result, words)
