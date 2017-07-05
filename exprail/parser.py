"""
Parser class definition
"""

from exprail.node import NodeType


class Parser:
    """The base class for other parsers"""

    def __init__(self, grammar, source):
        """
        Initialize the parser.
        :param grammar: a grammar object
        :param source: a parser object which provides the source token stream
        """
        self._grammar = grammar
        self._current_node = self._grammar.get_entry_node()
        self._source = source
        self._source.parse()
        self._ready = False
        self._token = None
        self._stacks = {'': []}

    def parse(self):
        """
        Parse the source stream while the parser has not become ready.
        :return: None
        """
        self._ready = False
        while not self.is_ready():
            token = self._source.get_token()
            self.choose_next_node(token)
            self.process_token(token)

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
        raise NotImplementedError('The token validation method has not implemented!')

    def get_finish_token(self):
        """
        Returns with the finish token of the parser.
        :return: a token object
        """
        raise NotImplementedError('The finish token has not implemented!')

    def show_info(self, message, token):
        """
        Show information about the current state of parsing.
        :param message: the message of the node
        :param token: the current token object
        :return: None
        """
        print('INFO: {}'.format(message))

    def show_error(self, message, token):
        """
        Show error in the parsing process. It stops the parsing process.
        :param message:
        :param token:
        :return:
        """
        print('ERROR: {}'.format(message))

    def transform(self, transformation, token):
        """
        Transform the token to an other token.
        :param transformation: the transformation described as a string
        :param token: the original token object
        :return: the transformed token object
        """
        return token

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
        self._stacks[stack_name].append(token.value)

    def clean_stack(self, stack_name, token):
        """
        Clean the given stack
        :param stack_name: the name of the stack as a string
        :param token: the current token
        :return: None
        """
        self._stacks[stack_name] = []

    def is_ready(self):
        """
        Signs that the processing has finished.
        :return: True, when the processing has finished, else False
        """
        return self._ready

    def choose_next_node(self, token):
        """
        Choose the next node and set it as the current node.
        :param token: the current token
        :return: None
        """
        # TODO: Choose the next node of the grammar graph!
        pass

    def collect_available_nodes(self):
        """
        Collect the available nodes from the current node.
        :return: the list of the available nodes
        """
        # TODO: Collect the available nodes from the grammar graph!
        pass

    def process_token(self, token):
        """
        Process the token according to the current node.
        :param token: a token object
        :return: None
        """
        node_type = self._current_node.type
        node_value = self._current_node.value
        if node_type is NodeType.FINISH:
            self._token = self.get_finish_token()
            self._ready = True
        elif node_type is NodeType.INFO:
            self.show_info(node_value, token)
        elif node_type is NodeType.ERROR:
            self.show_error(node_value, token)
        elif node_type is NodeType.TRANSFORMATION:
            self._current_node = self.transform(node_value, token)
        elif node_type is NodeType.OPERATION:
            self.operate(node_value, token)
        elif node_type is NodeType.STACK:
            self.push_stack(node_value, token)
        elif node_type is NodeType.CLEAN:
            self.clean_stack(node_value, token)
        elif node_type is NodeType.TOKEN:
            self._source.parse()
