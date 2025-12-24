from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from app.repository import init_store
from app.core.config import config

log = getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    store = await init_store()
    if not config.local_storage:
        log.info("Use minio storage with url %s", config.minio.url)
        await store.fiels.connect()
    else:
        log.info("Use local storage with path %s", config.local_storage_dir)

    await store.centrifugo.run_worker()
        
    yield
    await store.redis.close()
    await store.centrifugo.stop_worker()
