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
    INFO = 'info'
    ERROR = 'error'
    TRANSFORMATION = 'transformation'
    OPERATION = 'operation'
    STACK = 'stack'
    CLEAN = 'clean'
    GROUND = 'ground'
    ROUTER = 'router'
    TOKEN = 'token'


class Node:
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

    def __repr__(self):
        return '<Node({}, {})>'.format(self._type, self._value)

    def __eq__(self, other):
        return self.type is other.type and self.value == other.value

    def __hash__(self):
        return hash((self._type, self._value))
