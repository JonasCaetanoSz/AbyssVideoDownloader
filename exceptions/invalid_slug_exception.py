class InvalidSlugException(Exception):

    def __init__(self, message="Slug do vídeo inválido"):
        super().__init__(message)