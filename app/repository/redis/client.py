
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

    async def close(self):  
        await self.client.close()