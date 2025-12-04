from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete, insert, select, update, and_, func
from app.lib.log import log_call
from app.models import QuestionTagsORM
from sqlalchemy.orm import joinedload, selectinload
from app.models import QuestionORM, QuestionLikeORM, TagORM
from app.models.answers import AnswerORM
from app.models.users import UserORM

from app.repository.db.client import PostgresClient


class QuestionRepo:
    questions_options = (
                     joinedload(QuestionORM.author).joinedload(UserORM.profile), 
                     joinedload(QuestionORM.tags), 
                     joinedload(QuestionORM.answers)
                    )
    
    def __init__(self, pg: PostgresClient):
        self.pg = pg

    @log_call
    async def get_questions_order_by_datetime(self, limit: int = 10, offset: int =0) -> list[QuestionORM]:
        query = select(QuestionORM).order_by(QuestionORM.created_at.desc()).options(
            *self.questions_options
        )
        query = query.limit(limit).offset(offset)

        raw = await self.pg._execute(query)
        questions = raw.scalars().unique().all()
        print(questions)
        return list(questions)

    @log_call
    async def get_questions_order_by_hots(self, limit: int = 10, offset: int =0) -> list[QuestionORM]:
        query = select(QuestionORM).order_by(QuestionORM.likes_count.desc()).options(
            *self.questions_options
        )
        query = query.limit(limit).offset(offset)

        raw = await self.pg._execute(query)
        questions = raw.scalars().unique().all()
        return list(questions)
    
    @log_call
    async def create_question_like(self, user_id: int, question_id: int):
        query_insert = insert(QuestionLikeORM).values(user_id=user_id, question_id=question_id)
        query_update = update(QuestionORM).where(QuestionORM.id==question_id).values(likes_count=QuestionORM.likes_count+1)

        async with self.pg.session.begin() as tr:
            await tr.session.execute(query_insert)
            await tr.session.execute(query_update)

    @log_call
    async def delete_question_like(self, user_id: int, question_id: int):
        query_delete = delete(QuestionLikeORM).where(
            and_(QuestionLikeORM.user_id==user_id, QuestionLikeORM.question_id==question_id) 
        ).returning(QuestionLikeORM.question_id)
        query_update = update(QuestionORM).where(
            QuestionORM.id==question_id
        ).values(likes_count=QuestionORM.likes_count-1).returning(QuestionORM.id)

        async with self.pg.session.begin() as tr:
            res = await tr.session.execute(query_delete)
            if res.scalar_one_or_none():
                res = await tr.session.execute(query_update)
                if not res.scalar_one_or_none():
                    await tr.rollback()
                return 
            else:
                raise NoResultFound()
    @log_call
    async def get_question_by_id(self, question_id: int) -> QuestionORM | None:
        query = select(QuestionORM).where(QuestionORM.id == question_id).options(
                joinedload(QuestionORM.author).joinedload( UserORM.profile), 
                joinedload(QuestionORM.tags), 
                joinedload(QuestionORM.answers).joinedload(AnswerORM.author).joinedload( UserORM.profile)
        )
        raw = await self.pg._execute(query)
        question = raw.scalars().unique().one_or_none()
        return question

    @log_call
    async def get_questions_by_tag(self, tag_id: int, limit: int = 10, offset: int =0) -> list[QuestionORM]:
        query = (
            select(QuestionORM)
            .join(QuestionTagsORM, QuestionORM.id == QuestionTagsORM.question_id)
            .join(TagORM, QuestionTagsORM.tag_id == TagORM.id)
            .where(TagORM.id == tag_id)
            .options(*self.questions_options)
            )
        raw = await self.pg._execute(query)
        questions = raw.scalars().unique().all()
        return list(questions)


    @log_call
    async def get_questions_count(self, tag_id: int | None = None) -> int:
        query = select(func.count(QuestionORM.id.distinct()))
        if tag_id is not None:
            query = (
                query.join(QuestionTagsORM, QuestionORM.id==QuestionTagsORM.question_id)
                .join(TagORM, QuestionTagsORM.tag_id == TagORM.id)
                .where(TagORM.id == tag_id)
            )
        raw = await self.pg._execute(query)
        return raw.scalar_one()
    
    async def create_question(self, text: str, author_id: int, title: str) -> QuestionORM:
        async with self.pg.get_session() as session:
            q = QuestionORM(text=text, author_id=author_id, title=title)
            session.add(q)
            await session.commit()
            await session.refresh(q)
            return q

    async def create_answer(self, text: str, author_id: int, question_id: int) -> AnswerORM:
         async with self.pg.get_session() as session:
            a = AnswerORM(text=text, author_id=author_id, question_id=question_id)
            session.add(a)
            await session.commit()
            await session.refresh(a)
            return a

