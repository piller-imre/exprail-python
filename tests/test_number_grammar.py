import unittest

from exprail.classifier import Classifier
from exprail.grammar import Grammar
from exprail.parser import Parser
from exprail.source import SourceString


class NumberClassifier(Classifier):
    """Classify number symbol sets"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Distinguish digits, signs and the floating point.
        :param token_class: 'empty', '0', '0-9', '1-9', '.', '+', '-'
        :param token: the considered token
        :return: True, when the token is in the class, else False
        """
        if token.type == 'char':
            if token_class == '0-9':
                return token.value.isdigit()
            elif token_class == '1-9':
                return token.value in '123456789'
            elif len(token_class) == 1:
                return token.value == token_class
            elif token_class == 'empty':
                return False
            else:
                raise ValueError('Unhandled token class "{}"!'.format(token_class))
        elif token.type == 'empty':
            return token_class == 'empty'
        else:
            return False


class NumberParser(Parser):
    """Parse the input floating point number"""

    def __init__(self, grammar, source):
        super(NumberParser, self).__init__(grammar, source)
        self._result = {}

    @property
    def result(self):
        return self._result

    def operate(self, operation, token):
        """Print the token value on print operation."""
        if operation == 'negative':
            self._result['sign'] = '-'
        elif operation == 'non-negative':
            self._result['sign'] = '+'
        elif operation == 'save':
            self._result['integer'] = ''.join(self._stacks['integer'])
            if 'fraction' in self._stacks:
                self._result['fraction'] = ''.join(self._stacks['fraction'])
            if 'exponent' in self._stacks:
                self._result['exponent'] = ''.join(self._stacks['exponent'])
        else:
            raise ValueError('The "{}" is an invalid operation!'.format(operation))

    def show_error(self, message, token):
        """Show error in the parsing process."""
        raise ValueError(message)


class NumberGrammarTest(unittest.TestCase):
    """Number grammar tests with examples"""

    def test_empty_source(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'')
        parser = NumberParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Digit required!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_leading_plus_sign(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'+1234')
        parser = NumberParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Unnecessary plus sign!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_missing_digit(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'abc')
        parser = NumberParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Digit required!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_zero(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'0')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '+',
            'integer': '0'
        }
        self.assertEqual(parser.result, expected_result)

    def test_positive_integer(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'1234')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '+',
            'integer': '1234'
        }
        self.assertEqual(parser.result, expected_result)

    def test_negative_integer(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'-1234')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '-',
            'integer': '1234'
        }
        self.assertEqual(parser.result, expected_result)

    def test_only_fraction(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'0.5678')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '+',
            'integer': '0',
            'fraction': '5678'
        }
        self.assertEqual(parser.result, expected_result)

    def test_integer_and_fraction(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'1234.5678')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '+',
            'integer': '1234',
            'fraction': '5678'
        }
        self.assertEqual(parser.result, expected_result)

    def test_missing_fraction(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'1234.e')
        parser = NumberParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Missing fraction!')
        else:
            self.fail('The expected ValueError has not raised!')

    def test_only_exponent(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'0e100')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '+',
            'integer': '0',
            'exponent': '100'
        }
        self.assertEqual(parser.result, expected_result)

    def test_negative_exponent(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'0E-100')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '+',
            'integer': '0',
            'exponent': '-100'
        }
        self.assertEqual(parser.result, expected_result)

    def test_general_cases(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'1234.5678e9')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '+',
            'integer': '1234',
            'fraction': '5678',
            'exponent': '9'
        }
        self.assertEqual(parser.result, expected_result)

    def test_negated_cases(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'-1234.5678e-9')
        parser = NumberParser(grammar, source)
        parser.parse()
        expected_result = {
            'sign': '-',
            'integer': '1234',
            'fraction': '5678',
            'exponent': '-9'
        }
        self.assertEqual(parser.result, expected_result)

    def test_invalid_format(self):
        number_classifier = NumberClassifier()
        grammar = Grammar(filename='grammars/number.grammar', classifier=number_classifier)
        source = SourceString(r'-1234.5678e-9a')
        parser = NumberParser(grammar, source)
        try:
            parser.parse()
        except ValueError as error:
            self.assertEqual(str(error), 'Invalid number format!')
        else:
            self.fail('The expected ValueError has not raised!')
