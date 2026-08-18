from dataclasses import dataclass


@dataclass
class Resolution:

    value: str

    def __post_init__(self):
        self.value = self.value.lower()