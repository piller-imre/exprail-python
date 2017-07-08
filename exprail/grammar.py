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

    @property
    def expressions(self):
        return self._expressions

    def add_expression(self, name, expression):
        """Add new expression to the grammar."""
        self._expressions[name] = expression

    def load_from_file(self, filename):
        """Load the grammar from a grammar description."""
        self._expressions = loader.load_expressions(filename)

    def validate(self):
        """Validate the grammar."""
        validator.validate_grammar(self)

    def get_entry_node(self):
        """Get the entry node of the grammar."""
        for _, expression in self._expressions:
            if expression.is_entry_expression():
                return expression.get_start_node()
        raise RuntimeError('The entry expression is missing!')
