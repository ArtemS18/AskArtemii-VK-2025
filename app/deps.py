from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import SessionLocal

async def get_db():
    async with SessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]