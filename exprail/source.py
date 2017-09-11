"""
Source class definition
"""

from exprail.token import Token


class Source:
    """Character parser for input token stream"""

    def __init__(self, filename):
        """Open a source file as input."""
        self._input = open(filename, 'r')
        self._token = None
        self._ready = False

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

    @staticmethod
    def get_finish_token():
        """Provides the finish token."""
        return Token('empty', '')

    def get_token(self):
        """Get the last token of the source."""
        return self._token
