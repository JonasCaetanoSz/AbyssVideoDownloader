
class ResolutionNotAvailableException(Exception):

    def __init__(self, resolution):
        super().__init__(f"Resolution '{resolution.value}' is not available")