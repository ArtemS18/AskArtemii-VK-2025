from app.repository.minio.client import MinioClient


class UserAvatarRepository(MinioClient):
    bucket_name = "user-avatars"

    async def create_bucket(self):
        return await super().create_bucket(self.bucket_name)
    
    async def save_avatar_with_url(self, img: bytes, key: str, content_type: str = "image/png") -> str:
        await self.put_object(
            self.bucket_name, 
            key=key,
            body=img, 
            content_type=content_type
        )
        img_url = await self.generate_url(
            self.bucket_name,
            object_name=key, 
        )
        return img_url