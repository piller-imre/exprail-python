import unittest

from exprail.classifier import Classifier
from exprail.grammar import Grammar
from exprail.parser import Parser
from exprail.source import SourceString
from exprail.token import Token


class TokenizerClassifier(Classifier):
    """Classify the elements of the tokenizer sets"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Distinguish valid name characters and '"', '@', ';' characters.
        :param token_class: ['0-Z', '@', ';', '\\', '"', 'end']
        :param token: the considered token
        :return: True, when the token is in the class, else False
        """
        if token.type == 'char':
            if token_class == '0-Z':
                return token.value.isalnum()
            elif token_class == '@':
                return token.value == '@'
            elif token_class == ';':
                return token.value == ';'
            elif token_class == '\\':
                return token.value == '\\'
            elif token_class == '"':
                return token.value == '"'
        elif token.type == 'empty':
            return token_class == 'end'


class ParserClassifier(Classifier):
    """Classify the elements of the parser sets"""

    @staticmethod
    def is_in_class(token_class, token):
        """
        :param token_class: ['name', 'text', ';']
        :param token: the considered token
        :return: True, when the token is in the class, else False
        """
        return token.type == token_class


class FoliumTokenizer(Parser):
    """Tokenize the Folium data format"""

    def __init__(self, grammar, source):
        super(FoliumTokenizer, self).__init__(grammar, source)
        self._value = ''

    def operate(self, operation, token):
        """
        Save the name and text values
        :param operation: ['save', 'name', 'text', 'close']
        :param token: the considered token
        """
        if operation == 'save':
            self._value = ''.join(self._stacks[''])
        elif operation == 'name':
            self._token = Token('name', self._value)
            self._ready = True
        elif operation == 'text':
            self._token = Token('text', self._value)
            self._ready = True
        elif operation == 'close':
            self._token = Token(';', ';')
        else:
            raise ValueError('Undefined operation name! "{}"'.format(operation))

    def show_error(self, message, token):
        """Show error in the tokenization process."""
        raise ValueError(message)


class FoliumParser(Parser):
    """Parse the grammar of the Folium data format"""

    def __init__(self, grammar, source):
        super(FoliumParser, self).__init__(grammar, source)
        self._root = {}
        self._path = []
        self._parents = []

    def operate(self, operation, token):
        """
        Build a tree from elements
        :param token: the considered token
        :param operation: ['create', 'set_text', 'up']
        """
        if operation == 'create':
            if self._parents == []:
                self._parents = [self._root]
            self._parents[-1][token.value] = {}
            self._parents.append(token.value)
        elif operation == 'set_text':
            self._parents[-1][self._path[-1]] = token.value
        elif operation == 'up':
            self._parents.pop()
            self._path.pop()
        else:
            raise ValueError('Undefined operation name! "{}"'.format(operation))

    def show_error(self, message, token):
        """Show error in the parsing process."""
        raise ValueError(message)


class FoliumTokenizerTest(unittest.TestCase):
    pass


class FoliumParserTest(unittest.TestCase):
    pass
