class DomainNotFoundException(Exception):

    def __init__(self, domain: str):
        super().__init__( f"Domain not found: {domain}")