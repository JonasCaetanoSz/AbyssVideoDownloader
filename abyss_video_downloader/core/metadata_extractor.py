from ..core import slug_extractor

from ..exceptions import MetadataNotFoundException

from ..models import ( 
    VideoMetadata,
    EncryptedMedia
)

from ..utils import UrlValidator

from ..crypto import Decryptor


import requests
import json

def metadata_extractor(video_url:str) -> VideoMetadata :

    UrlValidator.validate(url=video_url)
    slug = slug_extractor(video_url=video_url).value
    api_endpoint = f"https://abysscdn.com/info/{slug}"

    headers = {
        'x-client-screen': '1366x768',
        'Referer': video_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'x-referer': 'https://embedplayabyss.top/',
    }


    response = requests.get(url=api_endpoint, headers=headers)

    if response.status_code != 200:
        raise MetadataNotFoundException()

    encrypted_data = EncryptedMedia( **json.loads(response.text) )
    descrypted_data = Decryptor.decrypt_video_data(encrypted_video_data=encrypted_data)
    return descrypted_data

