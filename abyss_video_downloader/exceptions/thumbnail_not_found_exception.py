class ThumbnailNotFoundException(Exception):

    def __init__(self, message="Thumbnail not found"):
        self.message = message
        super().__init__(self.message)