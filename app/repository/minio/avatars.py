from fastapi import UploadFile
from app.repository.minio.client import MinioClient
from logging import getLogger

log = getLogger(__name__)

class UserBucket(MinioClient):
    bucket_name = "user-avatars"

    async def connect(self):
        await self.create_public_bucket(self.bucket_name)

    async def save_avatar(self, file: UploadFile, user_id: int) -> str:
        body = await file.read()
        key = f"user_avatar_{user_id}"
        content_type = file.headers.get("content-type")

        await self.put_object(
            self.bucket_name,
            key=key,
            body=body,
            content_type=content_type
        )
        img_url = self.generate_public_url(
            self.bucket_name,
            object_name=key, 
        )
        return img_url

