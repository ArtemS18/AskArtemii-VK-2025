from fastapi import UploadFile
from app.repository.minio.client import MinioClient
from logging import getLogger

log = getLogger(__name__)


MAX_FILE_SIZE = 1024*1024*5

class FileSizeError(Exception):
    ...



class UserBucket(MinioClient):
    bucket_name = "user-avatars"

    async def connect(self):
        await self.create_public_bucket(self.bucket_name)
    @staticmethod
    def _get_size(file: UploadFile):
        if size := file.size:
            return size
        if size :=  file.headers.get("content-lenght"):
            return size
        else:
            raise FileSizeError
    
    def _validata_size(self, file: UploadFile):
        file_size = self._get_size(file)
        print(file_size)
        if file_size > MAX_FILE_SIZE:
            raise FileSizeError

    async def save_avatar(self, file: UploadFile, user_id: int) -> str:
        self._validata_size(file)

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

