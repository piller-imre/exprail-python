import unittest

from exprail.classifier import Classifier
from exprail.grammar import Grammar
from exprail.parser import Parser
from exprail.source import SourceString


class EscapedClassifier(Classifier):
    """Classify escape characters"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Distinguish escaped characters.
        :param token_class: '.', '"', '\'
        :param token: the value of the token
        :return: True, when the token is in the class, else False
        """
        if token.type == 'char':
            if token_class == '.':
                return True
            if token_class == '"\\':
                return token.value in ['"', '\\']
            else:
                return token_class == token.value
        else:
            return False


class EscapedParser(Parser):
    """Parse the input escaped string"""

    def __init__(self, grammar, source):
        super(EscapedParser, self).__init__(grammar, source)
        self._result = ''

    @property
    def result(self):
        return self._result

    def operate(self, operation, token):
        """Print the token value on print operation."""
        if operation == 'save':
            self._result = ''.join(self._stacks[''])
        else:
            raise ValueError('The "{}" is an invalid operation!'.format(operation))

    def show_error(self, message, token):
        """Show error in the parsing process."""
        raise ValueError(message)


class EscapedGrammarTest(unittest.TestCase):
    """Escaped grammar tests with examples"""

    def test_empty_source(self):
        escaped_classifier = EscapedClassifier()
        grammar = Grammar(filename='grammars/escaped.grammar', classifier=escaped_classifier)
        source = SourceString(r'')
        parser = EscapedParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Missing quote!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_without_escapes(self):
        escaped_classifier = EscapedClassifier()
        grammar = Grammar(filename='grammars/escaped.grammar', classifier=escaped_classifier)
        source = SourceString(r'"Simple string without escape characters"')
        parser = EscapedParser(grammar, source)
        parser.parse()
        self.assertEqual(parser.result, r'Simple string without escape characters')

    def test_multiple_escapes(self):
        escaped_classifier = EscapedClassifier()
        grammar = Grammar(filename='grammars/escaped.grammar', classifier=escaped_classifier)
        source = SourceString(r'"Some \" and \\ characters."')
        parser = EscapedParser(grammar, source)
        parser.parse()
        self.assertEqual(parser.result, r'Some " and \ characters.')

    def test_invalid_escape_character(self):
        escaped_classifier = EscapedClassifier()
        grammar = Grammar(filename='grammars/escaped.grammar', classifier=escaped_classifier)
        source = SourceString(r'"The \t is invalid here!"')
        parser = EscapedParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Invalid escape character!')
        else:
            self.fail('The expected ValueError has not raised!')
