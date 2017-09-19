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
        self._values = []

    def operate(self, operation, token):
        """Print the token value on print operation."""
        if operation == 'add':
            number = int(''.join(self._stacks['']))
            print('add: {}'.format(number))
            self._values.append(number)
        elif operation == 'show':
            print(self._values)
        else:
            raise ValueError('The "{}" is an invalid operation!'.format(operation))


if __name__ == '__main__':
    list_classifier = ListClassifier()
    grammar = Grammar(filename='integer_list.grammar', classifier=list_classifier)
    source = SourceString('[12, 34, 56]')
    parser = ListParser(grammar, source)
    parser.parse()
