from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import QuestionORM

async def get_questions_order_by_datetime(session: AsyncSession, limit: int = 10, offset: int =0) -> list[QuestionORM]:
    query = select(QuestionORM).order_by(QuestionORM.created_at)
    query = query.limit(limit).offset(offset)

    raw = await session.execute(query)
    questions = raw.scalars().all()
    return list(questions)

