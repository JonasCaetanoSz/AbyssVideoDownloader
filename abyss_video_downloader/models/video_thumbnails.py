from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VideoThumbnails:
    thumbnail: Optional[str] = None
    sprites: list[str] = field(default_factory=list)