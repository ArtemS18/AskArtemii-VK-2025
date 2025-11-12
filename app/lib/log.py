from functools import wraps
from logging import getLogger
import time
from typing import Any, Callable, Coroutine, TypeVar


type Function = Callable[..., Coroutine[Any, Any, None]]

def log_call(func: Function) -> Function:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        log = getLogger(func.__module__)
        start_time = time.perf_counter()
        log.debug("def %s called with args: %s, kwargs %s", func.__name__, args, kwargs)
        res = await func(*args, **kwargs)
        end_time = time.perf_counter() - start_time
        log.info("def %s executed: %0.3f ms", func.__name__, end_time*1000)
        return res 
    return wrapper

        