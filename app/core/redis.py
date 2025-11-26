from redis.asyncio import Redis

client = Redis(
    host='localhost', 
    port=6379, 
    db=0, 
    password='admin', 
    decode_responses=True
)

async def close():  
    await client.close()