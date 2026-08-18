from ..core.slug_extractor import slug_extractor

from ..models import VideoThumbnails

from ..exceptions import (
    ThumbnailNotFoundException,
    InvalidUrlException
)

from ..utils import UrlValidator

import requests


def thumbnail_extractor(video_url: str, max_sprites: int | None = None ) -> VideoThumbnails:


    UrlValidator.validate(url=video_url)

    slug = slug_extractor(video_url=video_url).value


    headers = {
        "Referer": "https://abysscdn.com/",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/151.0.0.0 Safari/537.36"
        )
    }


    data = VideoThumbnails()

    thumbnail_url = ( f"https://img.freeimagecdn.net/image/{slug}.jpg" )

    thumb_response = requests.get( thumbnail_url, headers=headers, timeout=10)

    if thumb_response.status_code != 200:
        raise ThumbnailNotFoundException("Thumbnail not found")
    
    data.thumbnail = thumbnail_url

    index = 0

    while True:

        if max_sprites and len(data.sprites) >= max_sprites:
            break

        sprite_url = ( f"https://img.freeimagecdn.net/image/{slug}/{index}.jpg")


        response = requests.get( sprite_url, headers=headers, timeout=10)

        if response.status_code != 200:
            break

        data.sprites.append(sprite_url)

        index += 1


    if not data.sprites:
        raise ThumbnailNotFoundException( "Sprite sheet not found")

    return data