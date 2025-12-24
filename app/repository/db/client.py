from sqlalchemy import Executable, Result, ScalarResult, Select, Sequence
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional, TypeVar
from sqlalchemy.engine.row import RowMapping

T = TypeVar("T")

class PostgresClient:
    def __init__(self, url: str):
        self.engine =  create_async_engine(url)
        self.session: AsyncSession | None = None

    async def connect(self):
        self.session = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()

    async def _execute(self, stmt: Executable) -> Result[Any]:
        if not self.session:
            raise ValueError("session is None")
        async with self.session() as session:  # type: AsyncSession
            res = await session.execute(stmt)
            await session.commit()
            return res

    async def scalar_one_or_none(self, stmt: Select[tuple[T]]) -> Optional[T]:
        res = await self._execute(stmt)
        return res.scalars().one_or_none()

    async def mapping(self, stmt: Select[Any]) -> RowMapping:
        res = await self._execute(stmt)
        return res.mappings().one()

    async def scalars_all(self, stmt: Select[tuple[T]]) -> Sequence[T]:
        res = await self._execute(stmt)
        return res.scalars().all()

    async def scalars(self, stmt: Select[tuple[T]]) -> ScalarResult[T]:
        res = await self._execute(stmt)
        return res.scalars()
        
        
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

