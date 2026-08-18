class VideoSourceNotFoundException(Exception):

    def __init__(self, message="Video source not found"):
        super().__init__(message)