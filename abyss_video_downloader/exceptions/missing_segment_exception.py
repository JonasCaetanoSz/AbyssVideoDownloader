class MissingSegmentException(Exception):

    def __init__(self, segment: int):
        self.segment = segment
        super().__init__(f"Missing segment: {segment}")