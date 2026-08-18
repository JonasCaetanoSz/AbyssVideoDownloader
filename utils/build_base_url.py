from models import (
    VideoFormat,
    VideoSource
)

from exceptions import DomainNotFoundException

def build_base_url(video_format: VideoFormat, video_source: VideoSource ):

    for domain in video_format.domains:

        if video_source.sub in domain:

            return "https://" + domain


    raise DomainNotFoundException(domain=video_source.sub)
