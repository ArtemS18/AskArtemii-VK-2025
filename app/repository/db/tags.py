from functools import lru_cache
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.lib.cache import cache_query, invalidate_query
from app.lib.log import log_call
from app.models.tags import TagORM
from app.repository.db.client import PostgresClient


class TagRepo():
    def __init__(self, pg: PostgresClient):
        self.pg = pg

    async def get_tag_by_id(self, tag_id: int) -> TagORM | None:
        query = (
            select(TagORM)
            .where(TagORM.id == tag_id)
            .limit(1)
        )
        raw = await self.pg._execute(query)
        tag = raw.scalar_one_or_none()
        return tag


    @log_call
    @cache_query("tags", ttl=600)
    async def get_tags_order_by_popular(self, limit=10) -> list[TagORM]:
        query = select(TagORM).order_by(TagORM.popular_count.desc()).limit(limit)
        raw = await self.pg._execute(query)
        tags = raw.scalars().all()
        return tags
    
    async def get_tags_by_names(self, names: list[str]) -> list[TagORM]:
        if not names:
            return []
        q = select(TagORM).where(TagORM.name.in_(names))
        raw = await self.pg._execute(q)
        return raw.scalars().all()

    async def create_tag(self, name: str) -> TagORM:
        tag = TagORM(name=name, popular_count=0)
        async with self.pg.get_session() as session:
            session.add(tag)
            await session.flush()
            await session.commit()
            return tag

    async def get_or_create_tags(self, names: list[str]) -> list[TagORM]:
        if not names:
            return []

        existing = await self.get_tags_by_names(names)
        by_name = {t.name: t for t in existing}

        result: list[TagORM] = []
        for name in names:
            tag = by_name.get(name)
            if tag is None:
                try:
                    tag = await self.create_tag(name)
                except IntegrityError:
                    await self.pg.session.rollback()
                    q = select(TagORM).where(TagORM.name == name).limit(1)
                    raw = await self.pg._execute(q)
                    tag = raw.scalar_one()
                by_name[name] = tag
            result.append(tag)

        return result
    
    @invalidate_query("tags")
    async def bump_popularity(self, tag_ids: list[int]) -> None:
        if not tag_ids:
            return
        q = (
            update(TagORM)
            .where(TagORM.id.in_(tag_ids))
            .values(popular_count=TagORM.popular_count + 1)
        )
        await self.pg._execute(q)
