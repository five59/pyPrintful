from .pfException import pfException


class pfAPIException(pfException):
    """API Exception Class"""

    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code
        self.message = message

    def __str__(self):
        return '%i - %s' % (self.code, self.message)
