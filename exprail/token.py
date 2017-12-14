"""
Token class definition
"""


class Token(object):
    """Represents a token with type and value"""

    def __init__(self, type, value):
        self._type = type
        self._value = value

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value
