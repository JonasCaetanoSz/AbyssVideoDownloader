from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoSource:

    label: str
    res_id: int
    size: int
    codec: str
    status: bool
    path: Optional[str] = None
    url: Optional[str] = None
    partSize: int = 0
    sub: str = ""