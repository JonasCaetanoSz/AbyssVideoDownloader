from dataclasses import dataclass, field


@dataclass
class MediaConfig:
    poster: bool = False
    preview: bool = False
    is_download: bool = False


@dataclass
class EncryptedMedia:
    title: str = ""
    has_bandwidth: bool = False
    is_raw: bool = False
    slug: str = ""
    md5_id: int = 0
    user_id: int = 0
    media: bytes = field(default_factory=bytes)
    config: MediaConfig = field(default_factory=MediaConfig)