"""
Source class definition
"""

from exprail.token import Token


class Source(object):
    """The base class for input streams"""

    def __init__(self):
        """Initialize the source object."""
        self._token = self.get_finish_token()
        self._ready = False

    @staticmethod
    def get_finish_token():
        """Provides the finish token."""
        return Token('empty', '')

    def get_token(self):
        """Get the last token of the source."""
        return self._token


class SourceString(Source):
    """Character parser for input stream with source string"""

    def __init__(self, value):
        """Save the string as the input."""
        super(SourceString, self).__init__()
        self._input = value
        self._index = 0

    def parse(self):
        """Select the next available character."""
        if self._index < len(self._input):
            self._token = Token('char', self._input[self._index])
            self._index += 1
        else:
            self._token = Source.get_finish_token()


class SourceFile(Source):
    """Character parser for input stream with source file"""

    def __init__(self, filename):
        """Open a source file as input."""
        super(SourceFile, self).__init__()
        self._input = open(filename, 'r')

    def parse(self):
        """Select the next available character."""
        if self._input is not None:
            c = self._input.read(1)
            if c:
                self._token = Token('char', c)
            else:
                self._token = Source.get_finish_token()
                self._input.close()
                self._input = None
        self._ready = True
