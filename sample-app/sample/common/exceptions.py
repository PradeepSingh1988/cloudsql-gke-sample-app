import logging


LOG = logging.getLogger(__name__)


class SampleException(Exception):
    """Base Sample Exception"""

    message = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if message:
            self.message = message

        try:
            self.message = self.message % kwargs
        except KeyError:

            LOG.exception("Exception in string format operation, " "kwargs: %s", kwargs)

    def __str__(self):
        return self.message


class UserNotFound(SampleException):
    message = "User not found."

class UserAlreadyExists(SampleException):
    message = "User Already exists"
