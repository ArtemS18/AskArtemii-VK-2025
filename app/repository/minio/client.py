import json
from typing import AsyncGenerator
from aiobotocore.session import get_session, AioBaseClient
from contextlib import asynccontextmanager
from botocore.exceptions import ClientError

class MinioClient:
    def __init__(self, url: str, access_key: str, secret_key: str):
        self.url = url
        self.access_key = access_key
        self.secret_key = secret_key
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[AioBaseClient, None]:

        async with self.session.create_client(
            "s3",
            endpoint_url=self.url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            verify=False
        ) as client:
            yield client

    async def create_public_bucket(self, bucket_name: str):
        policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AllowPublicRead",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
                    }
                ],
            }
       
        async with self.get_client() as client:
            try:
                await client.head_bucket(Bucket=bucket_name)
            except (ClientError) as e:
                if e.response['Error']['Code'] == '404':
                    await client.create_bucket(Bucket=bucket_name)
            await client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(policy),
            )

    async def put_object(self, bucket_name: str, key: str, body: bytes, content_type: str):
        async with self.get_client() as client:
            await client.put_object(Bucket=bucket_name, Key=key, Body=body, ContentType=content_type)

    async def generate_expiring_url(self, bucket_name: str, object_name: str, expires: int = 3000):
        async with self.get_client() as client:
            url = await client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket_name,
                        'Key': object_name
                    },
                    ExpiresIn=expires
                )
            return url
    def generate_public_url(self, bucket_name: str, object_name: str):
        return f"{self.url.rstrip("/")}/{bucket_name}/{object_name}"