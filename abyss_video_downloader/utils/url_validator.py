from ..exceptions import InvalidUrlException

from urllib.parse import urlparse


class UrlValidator:

    ALLOWED_HOST = "abysscdn.com"

    @staticmethod
    def validate(url: str) -> bool:

        url = url.lower()
        
        if not url:
            raise InvalidUrlException("URL is empty")

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            raise InvalidUrlException(
                "URL must use http or https"
            )

        if parsed.netloc != UrlValidator.ALLOWED_HOST:
            raise InvalidUrlException(
                "URL does not belong to Abyss CDN"
            )

        return True