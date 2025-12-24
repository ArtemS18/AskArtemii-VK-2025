from uuid import UUID
from app.core.redis import client
from app.lib.log import log_call
from app.repository.redis import key_builder
from app.repository.redis.client import RedisClient
from app.schemas.user import UserSession


USER_SESSION_TTL = int(60*30)
REFRESH_TTL = 60*10

class UserSessions(RedisClient):

    @log_call
    async def refresh_expire(self, key: str):
        ttl = await self.client.ttl(key)
        if ttl > 0 and ttl < REFRESH_TTL:
            ok = await self.client.expire(key, USER_SESSION_TTL)
            print(ok)

    @log_call
    async def create_user_session(self, session_key: str, user: UserSession) -> None:
        user_key = key_builder.get_session_key(session_key)
        await client.hset(user_key, mapping={
            "id": user.id, 
            "nickname": user.nickname, 
            "img_url": user.img_url,
            "csrf_token": str(user.csrf_token)
            }
        )
        await client.expire(name=user_key, time=USER_SESSION_TTL)

    @log_call
    async def get_session(self, session_key, with_refresh=True) -> UserSession | None:
        user_key = key_builder.get_session_key(session_key)
        raw = await client.hgetall(user_key)
        if not raw:
            return None
        await self.refresh_expire(user_key)
        
        return UserSession(
            id=raw["id"],
            nickname=raw["nickname"],
            img_url=raw["img_url"],
            csrf_token=UUID(raw["csrf_token"])
        )
        
    @log_call
    async def delete_session(self, session_key) -> None:
        user_key = key_builder.get_session_key(session_key)
        await client.delete(user_key)
        
    @log_call
    async def update_session(self, session_key, user: UserSession) -> None:
        user_key = key_builder.get_session_key(session_key)
        await client.hset(user_key, mapping={
            "id": user.id, 
            "nickname": user.nickname, 
            "img_url": user.img_url
            }
        )
        await self.refresh_expire(user_key)
