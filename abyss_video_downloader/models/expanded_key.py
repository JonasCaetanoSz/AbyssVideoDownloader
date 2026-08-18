from dataclasses import dataclass


@dataclass
class ExpandedKey:
    key: bytes
    counter: bytes