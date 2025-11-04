from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import config

engin = create_async_engine(config.db.url)

SessionLocal = async_sessionmaker(bind=engin, expire_on_commit=False)

async def init_db():
    from app.models.base import BaseORM
    import app.models # noqa: F401

    async with engin.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)

async def close():
    await engin.dispose()