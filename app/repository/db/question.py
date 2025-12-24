from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete, insert, select,  func
from app.lib.log import log_call
from app.models import QuestionTagsORM
from sqlalchemy.orm import joinedload, selectinload, with_loader_criteria
from app.models import QuestionORM, QuestionGradeORM, TagORM
from app.models.answers import AnswerORM
from app.models.grade import AnswerGradeORM
from app.models.users import UserORM

from app.repository.db.client import PostgresClient


class QuestionRepo:
    questions_options = (
                     joinedload(QuestionORM.author).joinedload(UserORM.profile), 
                     joinedload(QuestionORM.tags), 
                     joinedload(QuestionORM.answers),
                     
                    )
    
    def __init__(self, pg: PostgresClient):
        self.pg = pg

    @log_call
    async def search_questions_by_tsvector(self, search_query: str, *, limit:int = 10, offset: int = 0, user_id: int | None = None) -> list[QuestionORM]:
        tsq = func.websearch_to_tsquery("russian", search_query)
        query = (
            select(QuestionORM)
            .where(QuestionORM.search_vector.op("@@")(tsq)).order_by(func.ts_rank_cd(QuestionORM.search_vector, tsq))
            .options(*self.questions_options)
        )
        if user_id is not None:
            query = query.options(
                selectinload(QuestionORM.grade),
                with_loader_criteria(
                    QuestionGradeORM,
                    QuestionGradeORM.user_id == user_id,
                    include_aliases=True,
                )
            )
        query = query.limit(limit).offset(offset)
        res = await self.pg.scalars(query)
        return res.unique().all()
    
    async def get_count_search_questions(self, search_query: str) -> int:
        tsq = func.websearch_to_tsquery("russian", search_query)
        query = (
            select((func.count(QuestionORM.id))).where(QuestionORM.search_vector.op("@@")(tsq))
        )
        return await self.pg.scalar_one_or_none(query)
      

    @log_call
    async def get_questions_order_by_datetime(self, limit: int = 10, offset: int =0, user_id: int | None = None) -> list[QuestionORM]:
        query = select(QuestionORM).order_by(QuestionORM.created_at.desc()).options(
            *self.questions_options,
        )
        if user_id is not None:
            query = query.options(
                selectinload(QuestionORM.grade),
                with_loader_criteria(
                    QuestionGradeORM,
                    QuestionGradeORM.user_id == user_id,
                    include_aliases=True,
                )
            )
        query = query.limit(limit).offset(offset)

        raw = await self.pg._execute(query)
        questions = raw.scalars().unique().all()
        print(questions)
        return list(questions)

    @log_call
    async def get_questions_order_by_hots(self, limit: int = 10, offset: int =0, user_id: int | None = None) -> list[QuestionORM]:
        query = select(QuestionORM).order_by(QuestionORM.like_count.desc()).options(
            *self.questions_options,
            
        )
        if user_id is not None:
            query = query.options(
                selectinload(QuestionORM.grade),
                with_loader_criteria(
                    QuestionGradeORM,
                    QuestionGradeORM.user_id == user_id,
                    include_aliases=True,
                )
            )
        query = query.limit(limit).offset(offset)

        raw = await self.pg._execute(query)
        questions = raw.scalars().unique().all()
        return list(questions)
    @log_call
    async def get_question_by_id(self, question_id: int, user_id: int | None = None) -> QuestionORM | None:
        query = select(QuestionORM).where(QuestionORM.id == question_id).options(
                joinedload(QuestionORM.author).joinedload( UserORM.profile), 
                joinedload(QuestionORM.tags), 
                joinedload(QuestionORM.answers).joinedload(AnswerORM.author).joinedload( UserORM.profile)
        )
        if user_id is not None:
            query = query.options(
                selectinload(QuestionORM.grade),
                with_loader_criteria(
                    QuestionGradeORM,
                    QuestionGradeORM.user_id == user_id,
                    include_aliases=True,
                )
            )
            query = query.options(
                joinedload(QuestionORM.answers).selectinload(AnswerORM.grade),
                with_loader_criteria(
                    AnswerGradeORM,
                    AnswerGradeORM.user_id == user_id,
                    include_aliases=True,
                )
            )
        raw = await self.pg._execute(query)
        question = raw.scalars().unique().one_or_none()
        return question

    @log_call
    async def get_questions_by_tag(self, tag_id: int, limit: int = 10, offset: int =0, user_id: int | None = None) -> list[QuestionORM]:
        query = (
            select(QuestionORM)
            .join(QuestionTagsORM, QuestionORM.id == QuestionTagsORM.question_id)
            .join(TagORM, QuestionTagsORM.tag_id == TagORM.id)
            .where(TagORM.id == tag_id)
            .options(*self.questions_options)
            )
        if user_id is not None:
            query = query.options(
                selectinload(QuestionORM.grade),
                with_loader_criteria(
                    QuestionGradeORM,
                    QuestionGradeORM.user_id == user_id,
                    include_aliases=True,
                )
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
    
    async def create_question(self, text: str, author_id: int, title: str, tags: list[TagORM] | None) -> QuestionORM:
        async with self.pg.get_session() as session:
            q = QuestionORM(text=text, author_id=author_id, title=title)
            if tags:
                q.tags = tags
            session.add(q)
            await session.commit()
            await session.refresh(q)
            return q

    async def create_answer(self, text: str, author_id: int, question_id: int) -> AnswerORM:
        async with self.pg.get_session() as session:
            a = AnswerORM(text=text, author_id=author_id, question_id=question_id)
            session.add(a)
            await session.flush()

            stmt = (
                select(AnswerORM)
                .where(AnswerORM.id == a.id)
                .options(selectinload(AnswerORM.author).selectinload(UserORM.profile))
            )
            res = await session.execute(stmt)
            a_full = res.scalar_one()

            await session.commit()
            return a_full

