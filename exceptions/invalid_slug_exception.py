class InvalidSlugException(Exception):

    def __init__(self, message="Invalid video slug"):
        super().__init__(message)