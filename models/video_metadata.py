from dataclasses import dataclass


@dataclass
class VideoMetadata:

    @dataclass
    class Config:
        poster: bool
        preview: bool
        isDownload: bool


    title: str
    hasBandwidth: bool
    isRaw: bool
    slug: str
    md5_id: int
    user_id: int
    media: str
    config: Config