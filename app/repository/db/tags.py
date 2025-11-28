from sqlalchemy import select
from app.core.db import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.log import log_call
from app.models.tags import TagORM


async def get_tag_by_id(session: AsyncSession, tag_id: int) -> TagORM | None:
    query = (
        select(TagORM)
        .where(TagORM.id == tag_id)
        .limit(1)
    )
    raw = await session.execute(query)
    tag = raw.scalar_one_or_none()
    return tag


@log_call
async def get_tags_order_by_popular(limit=10) -> list[TagORM]:
    async with SessionLocal() as session:
        query = select(TagORM).order_by(TagORM.popular_count.desc()).limit(limit)
        raw = await session.execute(query)
        tags = raw.scalars().all()
        return tags
