from functools import wraps
import pickle



def cache_query(query_key, ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from app.repository import get_store
            store = get_store()
            
            cached_result = await store.redis.cache.get(f"cache:{query_key}")
            if cached_result:
                print("HIT")
                return pickle.loads(cached_result)
            else:
                print("MISS")
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
            
            await store.redis.cache.delete(f"cache:{query_key}")
            print("INVALIDATE")
            result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator