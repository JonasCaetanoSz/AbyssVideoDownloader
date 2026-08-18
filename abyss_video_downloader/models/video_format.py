from dataclasses import dataclass

from .video_source import VideoSource


@dataclass
class VideoFormat:

    sources: list[VideoSource]
    domains: list[str]
    fristDatas: list


    def __post_init__(self):

        self.sources = [
            VideoSource(**source)
            if isinstance(source, dict)
            else source

            for source in self.sources
        ]