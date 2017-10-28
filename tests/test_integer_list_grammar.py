import unittest

from exprail.classifier import Classifier
from exprail.grammar import Grammar
from exprail.parser import Parser
from exprail.source import SourceString


class ListClassifier(Classifier):
    """Classify integer list tokens"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Distinguish the list elements
        :param token_class: '0-9', '[', ']', ',' or 'ws'
        :param token: the value of the token
        :return: True, when the token is in the class, else False
        """
        if token.type == 'empty':
            return False
        if len(token_class) == 1:
            return token.value == token_class
        elif token_class == '0-9':
            return token.value.isdigit()
        elif token_class == 'ws':
            return token.value == ' '
        else:
            raise ValueError('Unexpected token class!')


class ListParser(Parser):
    """Parse the input text and print the words"""

    def __init__(self, grammar, source):
        """Initialize the integer list parser."""
        super(ListParser, self).__init__(grammar, source)
        self._result = []

    @property
    def result(self):
        return self._result

    def operate(self, operation, token):
        """Print the token value on print operation."""
        if operation == 'add':
            number = int(''.join(self._stacks['']))
            self._result.append(number)
        elif operation == 'save':
            pass
        else:
            raise ValueError('The "{}" is an invalid operation!'.format(operation))

    def show_error(self, message, token):
        """Show error in the parsing process."""
        raise ValueError(message)


class IntegerListTest(unittest.TestCase):
    """Integer list grammar tests with examples"""

    def test_empty_source(self):
        list_classifier = ListClassifier()
        grammar = Grammar(filename='grammars/integer_list.grammar', classifier=list_classifier)
        source = SourceString('')
        parser = ListParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Missing [ character!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_invalid_leading_character(self):
        list_classifier = ListClassifier()
        grammar = Grammar(filename='grammars/integer_list.grammar', classifier=list_classifier)
        source = SourceString('invalid')
        parser = ListParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Missing [ character!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_empty_list(self):
        list_classifier = ListClassifier()
        grammar = Grammar(filename='grammars/integer_list.grammar', classifier=list_classifier)
        source = SourceString('[]')
        parser = ListParser(grammar, source)
        parser.parse()
        self.assertEqual(parser.result, [])

    def test_single_integer(self):
        list_classifier = ListClassifier()
        grammar = Grammar(filename='grammars/integer_list.grammar', classifier=list_classifier)
        source = SourceString('[1234]')
        parser = ListParser(grammar, source)
        parser.parse()
        self.assertEqual(parser.result, [1234])

    def test_multiple_integers(self):
        list_classifier = ListClassifier()
        grammar = Grammar(filename='grammars/integer_list.grammar', classifier=list_classifier)
        source = SourceString('[12, 34, 56]')
        parser = ListParser(grammar, source)
        parser.parse()
        self.assertEqual(parser.result, [12, 34, 56])

    def test_unexpected_character(self):
        list_classifier = ListClassifier()
        grammar = Grammar(filename='grammars/integer_list.grammar', classifier=list_classifier)
        source = SourceString('[12, 34o]')
        parser = ListParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Unexpected character!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_missing_space(self):
        list_classifier = ListClassifier()
        grammar = Grammar(filename='grammars/integer_list.grammar', classifier=list_classifier)
        source = SourceString('[12, 34,56]')
        parser = ListParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Missing space!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_missing_integer(self):
        list_classifier = ListClassifier()
        grammar = Grammar(filename='grammars/integer_list.grammar', classifier=list_classifier)
        source = SourceString('[12, 34, , 78]')
        parser = ListParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'An integer expected!')
        else:
            self.fail('The expected ValueError has not raised!')
