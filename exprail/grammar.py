"""
Grammar class definition
"""

from exprail import loader
from exprail import validator
from exprail.state import State


class Grammar(object):
    """Represents a grammar"""

    def __init__(self, filename=None, classifier=None):
        self._classifier = classifier
        self._expressions = {}
        if filename is not None:
            self.load_from_file(filename)
            self.validate()

    @property
    def classifier(self):
        return self._classifier

    @property
    def expressions(self):
        return self._expressions

    def set_classifier(self, classifier):
        """Set the token classifier of the grammar."""
        self._classifier = classifier

    def add_expression(self, name, expression):
        """Add new expression to the grammar."""
        self._expressions[name] = expression

    def load_from_file(self, filename):
        """Load the grammar from a grammar description."""
        self._expressions = loader.load_expressions(filename)

    def validate(self):
        """Validate the grammar."""
        validator.validate_grammar(self)

    def get_initial_state(self):
        """
        Get the initial state of the grammar.
        :return: the State object of the grammar
        """
        expression_name = self.get_entry_expression_name()
        node_id = self.expressions[expression_name].get_start_node_id()
        return State(self, expression_name, node_id, None)

    def get_entry_expression_name(self):
        """Get the name of the entry expression."""
        for expression_name, expression in self._expressions.items():
            if expression.is_entry_expression():
                return expression_name
        raise RuntimeError('The entry expression is missing!')
