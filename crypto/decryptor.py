import json

from models import (
    ExpandedKey,
    EncryptedMedia,
    VideoMetadata
)

from Crypto.Cipher import AES
import hashlib


class Decryptor:
    
    def decrypt_video_data( encrypted_video_data:EncryptedMedia) -> VideoMetadata:

        key = Decryptor.expandKey(video_data=encrypted_video_data)
        descrypted_media = Decryptor.decrypt_string_media( media=encrypted_video_data.media , expanded_key=key)
        descrypted_data = encrypted_video_data.__dict__
        descrypted_data["media"] = json.loads(descrypted_media)
        return VideoMetadata(**descrypted_data)
    

    @staticmethod
    def expandKey(video_data: EncryptedMedia) -> ExpandedKey:

        value = ( str(video_data.user_id) + ":" + str(video_data.slug ) + ":" + str(video_data.md5_id) )

        md5 = hashlib.md5( value.encode("utf-8") ).hexdigest()

        key_bytes = md5.encode("utf-8")

        counter = key_bytes[:16]

        return ExpandedKey( key=key_bytes, counter=counter)


    @staticmethod
    def decrypt_string_media(media: str, expanded_key:ExpandedKey) -> str:

        encrypted = bytes(
            ord(c)
            for c in media
        )


        cipher = AES.new(
            expanded_key.key,
            AES.MODE_CTR,
            initial_value=int.from_bytes(
                expanded_key.counter,
                byteorder="big"
            ),
            nonce=b""
        )


        decrypted = cipher.decrypt(encrypted)

        return decrypted.decode("utf-8")