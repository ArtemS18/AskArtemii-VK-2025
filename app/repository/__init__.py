from dataclasses import dataclass
from typing import Protocol

from fastapi import UploadFile

from app.core.config import config
from app.repository.centrifugo.client import CentrifugoCletnt
from app.repository.db.answer import AnswerRepo
from app.repository.db.client import PostgresClient
from app.repository.db.grade import GradesRepo
from app.repository.local_storage.local_storage import LocalFileStorage
from app.repository.redis.sessions import UserSessions
from app.repository.db.question import QuestionRepo
from app.repository.db.user import UserRepo
from app.repository.db.tags import TagRepo
from .minio.avatars import UserBucket

class FileRepo(Protocol):
    async def connect(self) -> None:
        ...
    async def save_avatar(self, file: UploadFile, user_id: int) -> str:
        ...

@dataclass
class Store:
    fiels: FileRepo
    redis: UserSessions
    centrifugo: CentrifugoCletnt

    quesion: QuestionRepo
    user: UserRepo
    tag: TagRepo
    grade: GradesRepo
    answer: AnswerRepo

_store: Store | None = None

async def init_store() -> Store:
    global _store
    if _store is None:
        pg = PostgresClient(config.db.url)

        await pg.connect()
        file_repo = UserBucket(
            config.minio.url, 
            config.minio.access_key, 
            config.minio.secret_key
        ) if not config.local_storage else LocalFileStorage() # TODO: add config for localfile storage

        
        _store = Store(
            fiels=file_repo,
            redis=UserSessions(), # TODO: add config for redis
            quesion=QuestionRepo(pg),
            user=UserRepo(pg),
            tag=TagRepo(pg),
            grade=GradesRepo(pg),
            answer=AnswerRepo(pg),
            centrifugo=CentrifugoCletnt(
                config.centrifugo_jwt_key,
                config.centrifugo_api_key,
                config.centrifugo_api_url
            )
        )
    return _store

def get_store() -> Store: 
    if _store is not None:
        return _store
    else:
        raise ValueError("Store is None")
