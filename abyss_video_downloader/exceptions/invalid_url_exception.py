class InvalidUrlException(Exception):

    def __init__(self, message="Invalid URL"):
        super().__init__(message)