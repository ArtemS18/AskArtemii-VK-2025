from uuid import UUID
from app.core.redis import client
from app.repository.redis import key_builder
from app.repository.redis.client import RedisClient
from app.schemas.user import UserSession

class UserSessions(RedisClient):
    async def create_user_session(self, session_key: str, user: UserSession) -> None:
        user_key = key_builder.get_session_key(session_key)
        await client.hset(user_key, mapping={
            "id": user.id, 
            "nickname": user.nickname, 
            "img_url": user.img_url,
            "csrf_token": str(user.csrf_token)
            }
        )
        ttl = 60*60
        await client.expire(name=user_key, time=ttl)

    async def get_session(self, session_key) -> UserSession | None:
        user_key = key_builder.get_session_key(session_key)
        raw = await client.hgetall(user_key)
        if not raw:
            return None
        return UserSession(
            id=raw["id"],
            nickname=raw["nickname"],
            img_url=raw["img_url"],
            csrf_token=UUID(raw["csrf_token"])
        )
        
    async def delete_session(self, session_key) -> None:
        user_key = key_builder.get_session_key(session_key)
        await client.delete(user_key)
        

    async def update_session(self, session_key, user: UserSession) -> None:
        user_key = key_builder.get_session_key(session_key)
        await client.hset(user_key, mapping={
            "id": user.id, 
            "nickname": user.nickname, 
            "img_url": user.img_url
            }
        )
