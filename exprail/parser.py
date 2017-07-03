"""
Parser class definition
"""


class Parser:
    """The base class for other parsers"""

    def __init__(self):
        pass

    def parse(self):
        pass

    def is_valid_token(self, node_class, node_filter, token):
        pass

    def show_info(self, message, token):
        pass

    def show_error(self, message, token):
        pass

    def transform(self, transformation, token):
        pass

    def operate(self, operation, token):
        pass

    def push_stack(self, stack_name, token):
        pass

    def clean_stack(self, stack_name, token):
        pass
