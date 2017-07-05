"""
Parser class definition
"""


class Parser:
    """The base class for other parsers"""

    def __init__(self, grammar, source):
        """
        Initialize the parser.
        :param grammar: a grammar object
        :param source: a parser object which provides the source token stream
        """
        self._grammar = grammar
        self._source = source
        self._current_node = grammar.get_entry_node()
        self._ready = False
        self._token = None
        self._stacks = {'': []}

    def parse(self):
        """
        Parse the source stream while the parser has not become ready.
        :return: None
        """
        pass

    def get_token(self):
        """
        Get the recently parsed token.
        :return: a token object
        """
        return self._token

    def get_next_token(self):
        """
        A convenience method for parsing and getting the last token at one step.
        :return: a token object
        """
        self.parse()
        return self.get_token()

    def is_valid_token(self, token_filter, token):
        """
        Check that the processed token is valid according the the node.
        :param token_filter: a string for describing a valid token, for example 'keyword: class'
        :param token: a token object
        :return: True, when the token is valid, else False
        """
        pass

    def is_ready(self):
        """
        Signs that the processing has finished.
        :return: True, when the processing has finished, else False
        """
        pass

    def show_info(self, message, token):
        """
        Show information about the current state of parsing.
        :param message: the message of the node
        :param token: the current token object
        :return: None
        """
        pass

    def show_error(self, message, token):
        """
        Show error in the parsing process. It stops the parsing process.
        :param message:
        :param token:
        :return:
        """
        pass

    def transform(self, transformation, token):
        """
        Transform the token to an other token.
        :param transformation: the transformation described as a string
        :param token: the original token object
        :return: the transformed token object
        """
        pass

    def operate(self, operation, token):
        """
        Fulfil the required operation.
        :param operation: the name of the operation as a string
        :param token: the current token
        :return: None
        """
        pass

    def push_stack(self, stack_name, token):
        """
        Push the token value onto the stack.
        :param stack_name: the name of the stack as a string
        :param token: the current token
        :return: None
        """
        pass

    def clean_stack(self, stack_name, token):
        """
        Clean the given stack
        :param stack_name: the name of the stack as a string
        :param token: the current token
        :return: None
        """
        pass
