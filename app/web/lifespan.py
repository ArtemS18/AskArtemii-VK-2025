from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    yield
    await db.close()