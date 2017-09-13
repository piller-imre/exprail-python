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

    def operate(self, operation, token):
        """Print the token value on print operation."""
        if operation == 'print':
            print(''.join(self._stacks['']))
        else:
            raise ValueError('The "{}" is an invalid operation!'.format(operation))


if __name__ == '__main__':
    escaped_classifier = EscapedClassifier()
    grammar = Grammar(filename='escaped.grammar', classifier=escaped_classifier)
    source = SourceString(r'"Some \" and \\ characters."')
    parser = EscapedParser(grammar, source)
    parser.parse()
