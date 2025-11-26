from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core import db, redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    yield
    await db.close()
    await redis.close()