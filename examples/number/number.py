from exprail.classifier import Classifier
from exprail.grammar import Grammar
from exprail.parser import Parser
from exprail.source import Source


class NumberClassifier(Classifier):
    """Classify number symbol sets"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Distinguish digits and signs and the floating point.
        :param token_class: '0', '0-9', '1-9', '.', '+', '-'
        :param token: the value of the token
        :return: True, when the token is in the class, else False
        """
        if token.type == 'char':
            if token_class == '0-9':
                return token.value.isdigit()
            elif token_class == '1-9':
                return token.value in '123456789'
            elif len(token_class) == 1:
                return token.value == token_class
        else:
            return False


class NumberParser(Parser):
    """Parse the input floating point number"""

    def operate(self, operation, token):
        """Print the token value on print operation."""
        if operation == 'print':
            print(''.join(self._stacks['']))
        else:
            raise ValueError('The "{}" is an invalid operation!'.format(operation))


if __name__ == '__main__':
    number_classifier = NumberClassifier()
    grammar = Grammar(filename='number.grammar', classifier=number_classifier)
    source = Source('number.txt')
    parser = NumberParser(grammar, source)
    parser.parse()
