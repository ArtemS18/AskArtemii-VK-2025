from app.core.redis import client
from app.repository.redis import key_builder
from app.schemas.user import User
from datetime import datetime, timedelta


async def create_session(session_key, user: User) -> None:
    user_key = key_builder.get_session_key(session_key)
    await client.hset(user_key, mapping={
        "id": user.id, 
        "nickname": user.nickname, 
        "img_url": user.img_url
        }
    )
    ttl = 1 * 60
    await client.expire(name=user_key, time=ttl)

async def get_session(session_key) -> User | None:
    user_key = key_builder.get_session_key(session_key)
    raw = await client.hgetall(user_key)
    if not raw:
        return None
    return User(
        id=raw["id"],
        nickname=raw["nickname"],
        img_url=raw["img_url"]
    )
    
async def delete_session(session_key) -> None:
    user_key = key_builder.get_session_key(session_key)
    await client.delete(user_key)
    

async def update_session(session_key, user: User) -> None:
    user_key = key_builder.get_session_key(session_key)
    await client.hset(user_key, mapping={
        "id": user.id, 
        "nickname": user.nickname, 
        "img_url": user.img_url
        }
    )
