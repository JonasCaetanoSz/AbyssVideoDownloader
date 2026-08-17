from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class VideoMetadata:

    @dataclass
    class Config:
        poster: bool
        preview: bool
        isDownload: bool
        logo: Optional[dict] = None


    title: str
    hasBandwidth: bool
    isRaw: bool
    slug: str
    md5_id: int
    user_id: int
    media: str
    config: Config
    danmu: Optional[dict] = None

    def to_dict(self):
        return asdict(self)