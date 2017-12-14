"""
Parser class definition
"""

from exprail.node import NodeType
from exprail import router
from exprail.state import State


class Parser(object):
    """The base class for other parsers"""

    def __init__(self, grammar, source):
        """
        Initialize the parser.
        :param grammar: a grammar object
        :param source: a parser object which provides the source token stream
        """
        self._grammar = grammar
        self._state = grammar.get_initial_state()
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
        while not self._ready:
            token = self._source.get_token()
            self._state = router.find_next_state(self._state, token)
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

    def get_finish_token(self):
        """
        Returns with the finish token of the parser.
        NOTE: It must be implemented when the parser provides tokens as outputs!
        :return: a token object
        """
        pass

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
        if stack_name not in self._stacks:
            self._stacks[stack_name] = []
        self._stacks[stack_name].append(token.value)

    def clean_stack(self, stack_name, token):
        """
        Clean the given stack
        :param stack_name: the name of the stack as a string
        :param token: the current token
        :return: None
        """
        self._stacks[stack_name] = []

    def process_token(self, token):
        """
        Process the token according to the current node.
        :param token: a token object
        :return: None
        """
        node_type = self._state.node.type
        node_value = self._state.node.value
        if node_type is NodeType.EXPRESSION:
            expression_name = self._state.node.value
            node_id = self._state.grammar.expressions[expression_name].get_start_node_id()
            self._state = State(self._state.grammar, expression_name, node_id, self._state)
        elif node_type is NodeType.FINISH:
            if self._state.return_state is None:
                self._token = self.get_finish_token()
                self._ready = True
        elif node_type is NodeType.INFO:
            self.show_info(node_value, token)
        elif node_type is NodeType.ERROR:
            self.show_error(node_value, token)
        elif node_type is NodeType.TRANSFORMATION:
            self._token = self.transform(node_value, token)
        elif node_type is NodeType.OPERATION:
            self.operate(node_value, token)
        elif node_type is NodeType.STACK:
            self.push_stack(node_value, token)
        elif node_type is NodeType.CLEAN:
            self.clean_stack(node_value, token)
        elif node_type in [NodeType.TOKEN, NodeType.EXCEPT_TOKEN, NodeType.DEFAULT_TOKEN]:
            self._source.parse()
