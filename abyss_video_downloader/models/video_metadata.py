from dataclasses import dataclass, asdict
from typing import Optional

from .resolution import Resolution
from .video_format import VideoFormat


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
    media: dict[str, VideoFormat]
    config: Config
    danmu: Optional[dict] = None


    def __post_init__(self):

        self.media = {
            video_ext: VideoFormat(**video_format)
            if isinstance(video_format, dict)
            else video_format

            for video_ext, video_format in self.media.items()
        }


    def to_dict(self):
        return asdict(self)


    def has_resolution(self, video_ext: str, resolution: Resolution ) -> bool:

        video_format = self.media.get(video_ext)

        if not video_format:
            return False


        for source in video_format.sources:

            if source.label == resolution.value:
                return True


        return False