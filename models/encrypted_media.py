from dataclasses import dataclass
from typing import Optional


@dataclass
class EncryptedMedia:

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
    media: dict
    config: Config
    danmu: Optional[dict] = None

    def has_resolution(self , video_ext:str, resolution:Resolution ) -> bool:

        if self.media and self.media.get(video_ext):
            for  source_item in self.media.get(video_ext).get("sources", {}):
                if source_item.get("label", None) == resolution.value:
                    return True

        return False

    