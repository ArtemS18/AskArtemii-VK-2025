from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from typing import AsyncGenerator

class PostgresClient:
    def __init__(self, url: str):
        self.engine =  create_async_engine(url)
        self.session: AsyncSession | None = None

    async def connect(self):
        self.session = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()

    async def _execute(self, query):
        if self.session:
            async with self.session() as session:
                return await session.execute(query)
        else:
            raise ValueError("session is None")
        
    @asynccontextmanager
    async def get_session(self, with_tr: bool = False) ->AsyncGenerator[AsyncSession, None]:
        if self.session:
            async with self.session() as session:
                yield session
        else:
            raise ValueError("session is None")
    
        
    async def init_db(self):
        from app.models.base import BaseORM
        import app.models # noqa: F401

        async with self.engine.begin() as conn:
            await conn.run_sync(BaseORM.metadata.create_all)

    async def drop_db(self):
            from app.models.base import BaseORM
            import app.models # noqa: F401

            async with self.engine.begin() as conn:
                await conn.run_sync(BaseORM.metadata.drop_all)

