# https://docs.python.org/3/tutorial/errors.html

class LoopyError(Exception):
    pass

class LoopyFileError(LoopyError):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, filename, message):
        self.filename = filename
        self.message = message


class LoopyParsingError(LoopyError):
    def __init__(self, filename, message):
        self.filename = filename
        self.message = message


class LoopyValueError(LoopyError):
    def __init__(self, message):
        self.message = message


class LoopyArgumentError(LoopyError):
    def __init__(self, message):
        self.message = message


class LoopyInputError(LoopyError):
    def __init__(self, message):
        self.message = message