from models.expanded_key import ExpandedKey
from models.encrypted_media import EncryptedMedia

import hashlib


class Decryptor:
    def decryptVideoData(video_data:str) -> dict:
        pass

    def expandKey(video_data: EncryptedMedia) -> ExpandedKey:

        value = ( str(video_data.user_id) + ":" + str(video_data.slug ) + ":" + str(video_data.md5_id) )

        md5 = hashlib.md5( value.encode("utf-8") ).hexdigest()

        key_bytes = md5.encode("utf-8")

        counter = key_bytes[:16]

        return ExpandedKey( key=key_bytes, counter=counter)