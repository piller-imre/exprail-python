"""
Node class definition
"""

from enum import Enum


class NodeType(Enum):
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

    def __init__(self, type, value):
        self._type = type
        self._value = value
        self._targets = []

    @property
    def type(self):
        return self.type

    @property
    def value(self):
        return self.value
