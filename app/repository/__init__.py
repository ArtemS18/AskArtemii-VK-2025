from dataclasses import dataclass

from app.core.config import config
from app.repository.db.client import PostgresClient
from app.repository.redis.sessions import UserSessions
from app.repository.db.question import QuestionRepo
from app.repository.db.user import UserRepo
from app.repository.db.tags import TagRepo
from .minio.avatars import UserBucket

@dataclass
class Store:
    minio: UserBucket
    redis: UserSessions

    quesion: QuestionRepo
    user: UserRepo
    tag: TagRepo

_store: Store | None = None

async def init_store() -> Store:
    global _store
    if _store is None:
        pg = PostgresClient(config.db.url)

        await pg.connect()
        
        _store = Store(
            minio=UserBucket(
                config.minio.url, 
                config.minio.access_key, 
                config.minio.secret_key
            ),
            redis=UserSessions(), # TODO: add config for redis

            quesion=QuestionRepo(pg),
            user=UserRepo(pg),
            tag=TagRepo(pg)
        )
    return _store

def get_store() -> Store: 
    if _store is not None:
        return _store
    else:
        raise ValueError("Store is None")
