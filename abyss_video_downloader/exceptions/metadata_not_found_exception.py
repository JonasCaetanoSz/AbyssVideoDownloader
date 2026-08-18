class MetadataNotFoundException(Exception):

    def __init__(self, message="Metadata not found"):
        self.message = message
        super().__init__(self.message)