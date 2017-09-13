from exprail.classifier import Classifier
from exprail.grammar import Grammar
from exprail.parser import Parser
from exprail.source import SourceFile


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

    def operate(self, operation, token):
        """Print the token value on print operation."""
        if operation == 'print':
            print(''.join(self._stacks['']))
        else:
            raise ValueError('The "{}" is an invalid operation!'.format(operation))


if __name__ == '__main__':
    ws_classifier = WsClassifier()
    grammar = Grammar(filename='words.grammar', classifier=ws_classifier)
    source = SourceFile('words.txt')
    parser = WsParser(grammar, source)
    parser.parse()
