"""
Classifier class definition
"""


class Classifier(object):
    """Represents the base class of the token classifiers."""

    @staticmethod
    def is_in_class(token_class, token):
        """
        Check that whether the token is in the class or not.
        :param token_class: the name of the token class as a string
        :param token: the considered token
        :return: True, when the token is in the class, else False
        """
        raise NotImplementedError('The classifier does not implemented!')
