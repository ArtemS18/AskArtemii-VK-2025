
from sqlalchemy import select
from app.repository.db.client import PostgresClient
from app.models import AnswerORM

class AnswerRepo:
    
    def __init__(self, pg: PostgresClient):
        self.pg = pg

    async def get_answer_by_id(self, answer_id: int):
        q = select(AnswerORM).where(AnswerORM.id == answer_id)
        return await self.pg.scalar_one_or_none(q)
    
    async def get_answer_by_id(self, answer_id: int):
        q = select(AnswerORM).where(AnswerORM.id == answer_id)
        return await self.pg.scalar_one_or_none(q)