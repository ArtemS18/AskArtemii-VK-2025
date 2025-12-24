from functools import wraps
from logging import getLogger
import pickle



def cache_query(query_key, ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from app.repository import get_store
            store = get_store()
            log = getLogger(__name__)
            
            cached_result = await store.redis.cache.get(f"cache:{query_key}")
            if cached_result:
                log.info(f"Cache '{query_key}': HIT", stacklevel=3)
                return pickle.loads(cached_result)
            else:
                log.info(f"Cache '{query_key}': MISS", stacklevel=3)
            result = await func(*args, **kwargs)
            data = pickle.dumps(result)
            await store.redis.cache.setex(f"cache:{query_key}", ttl, data)
            return result
        return wrapper
    return decorator

def invalidate_query(query_key):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from app.repository import get_store
            store = get_store()
            log = getLogger(__name__)
            
            await store.redis.cache.delete(f"cache:{query_key}")
            log.info(f"Cache '{query_key}': INVALIDATE", stacklevel=3)
            result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator