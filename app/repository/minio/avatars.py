from app.repository.minio.client import MinioClient
from logging import getLogger

log = getLogger(__name__)


class UserAvatarRepository(MinioClient):
    bucket_name = "user-avatars"

    async def create_bucket(self):
        return await super().create_public_bucket(self.bucket_name)
    
    
    async def save_avatar_with_url(self, img: bytes, key: str, content_type: str = "image/png") -> str:
        log.info("%s, %s", key, content_type)
        await self.put_object(
            self.bucket_name, 
            key=key,
            body=img, 
            content_type=content_type
        )
        img_url = self.generate_public_url(
            self.bucket_name,
            object_name=key, 
        )
        log.info("url: %s", img_url)
        return img_url