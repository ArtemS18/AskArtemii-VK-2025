from sqlalchemy import select
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
    async def get_tags_order_by_popular(self, limit=10) -> list[TagORM]:
        query = select(TagORM).order_by(TagORM.popular_count.desc()).limit(limit)
        raw = await self.pg._execute(query)
        tags = raw.scalars().all()
        return tags
