from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.repository import init_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    store = await init_store()
    await store.minio.connect()
    yield
    await store.redis.close()
