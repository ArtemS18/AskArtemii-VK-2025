
from typing import Any
from redis.asyncio import Redis


class RedisClient():
    def __init__(
            self, 
            host: str = 'localhost', 
            port: int = 6379, 
            db: int = 0, 
            pwd: str = 'admin', 
            decode_response: bool = True
        ):
        self.client = Redis(
            host=host, 
            port=port, 
            db=db, 
            password=pwd, 
            decode_responses=decode_response
        )
        self.cache = Redis(
            host=host, 
            port=port, 
            db=db+1, 
            password=pwd, 
            decode_responses=False,
        )

    async def close(self):  
        await self.client.close()

    async def set_cache(self, funcname: str, res: Any):
        await self.client.set(f"cache:{funcname}", res, ex=3000)

    async def get_cache(self, funcname: str):
        res = await self.client.get(f"cache:{funcname}")
        return res

