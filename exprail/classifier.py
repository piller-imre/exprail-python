"""
Classifier class definition
"""


class Classifier:
    """Represents the base class of the token classifiers."""

    def is_in_class(self, token):
        """
        Check that whether the token is in the class or not.
        :param token: the considered token
        :return: True, when the token is in the class, else False
        """
        raise NotImplementedError('The classifier does not implemented!')
