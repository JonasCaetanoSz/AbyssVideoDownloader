from ..exceptions.invalid_slug_exception import InvalidSlugException
from ..exceptions.invalid_url_exception import InvalidUrlException

from ..utils import UrlValidator

from ..models import VideoSlug

from urllib.parse import urlparse, parse_qs

def slug_extractor(video_url: str) -> VideoSlug:
    try:
        UrlValidator.validate(url=video_url)
    except InvalidUrlException as e :
        print("error: " + str(e))
        return False
    
    parsed = urlparse(video_url)
    params = parse_qs(parsed.query)
    slug = params.get("v")

    if not slug:
        raise InvalidSlugException(f"Slug not found for URL: [{video_url}] ")

    return VideoSlug(value=slug[0])
