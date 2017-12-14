"""
Node class definition
"""

from enum import Enum


class NodeType(Enum):
    """The possible types of the nodes in the expression graph"""

    START = 'start'
    FINISH = 'finish'
    CONNECTION = 'connection'
    EXPRESSION = 'expression'
    GROUND = 'ground'
    TOKEN = 'token'
    EXCEPT_TOKEN = 'except_token'
    DEFAULT_TOKEN = 'default_token'
    ROUTER = 'router'
    EXCEPT_ROUTER = 'except_router'
    DEFAULT_ROUTER = 'default_router'
    INFO = 'info'
    ERROR = 'error'
    OPERATION = 'operation'
    TRANSFORMATION = 'transformation'
    STACK = 'stack'
    CLEAN = 'clean'


class Node(object):
    """Represents a node of the syntax graph"""

    def __init__(self, type, value=''):
        self._type = NodeType(type)
        self._value = value

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def is_matchable(self):
        """
        Check that the node can be matched in the routing process.
        :return: True, when the route is matchable, else False
        """
        matchable_types = [
            NodeType.ROUTER,
            NodeType.EXCEPT_ROUTER,
            NodeType.TOKEN,
            NodeType.EXCEPT_TOKEN
        ]
        return self._type in matchable_types

    def is_default(self):
        """
        Check that the node can be used as a default route.
        :return: True, when the node is a default route, else False
        """
        default_types = [
            NodeType.DEFAULT_ROUTER,
            NodeType.DEFAULT_TOKEN,
            NodeType.FINISH
        ]
        return self._type in default_types

    def __repr__(self):
        return '<Node({}, {})>'.format(self._type, self._value)

    def __eq__(self, other):
        return self.type is other.type and self.value == other.value

    def __hash__(self):
        return hash((self._type, self._value))
