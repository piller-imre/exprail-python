"""
Grammar class definition
"""

from exprail import loader
from exprail import validator


class Grammar:
    """Represents a grammar"""

    def __init__(self, filename=None):
        self._expressions = {}
        if filename is not None:
            self.load_from_file(filename)
            self.validate()

    def load_from_file(self, filename):
        """Load the grammar from a grammar description."""
        self._expressions = loader.load_expressions(filename)

    def validate(self):
        """Validate the grammar."""
        validator.validate_grammar(self)

    def get_entry_node(self):
        """Get the entry node of the grammar."""
        pass
