from functools import wraps
from logging import getLogger
import time
from typing import Any, Callable, Coroutine, TypeVar

T = TypeVar("Function", bound= Callable[..., Coroutine[Any, Any, Any]])

def log_call( func: T) -> T:

    @wraps(func)
    async def wrapper(*args, **kwargs):
        log = getLogger(func.__module__)
        start_time = time.perf_counter()
        log.debug("def %s called with args: %s, kwargs %s", func.__name__, args, kwargs)
        res = await func(*args, **kwargs)
        end_time = time.perf_counter() - start_time
        log.info("def %s return <%.50s...> executed: %0.3f ms ", func.__name__, res, end_time*1000, stacklevel=2)
        return res 
    return wrapper

        