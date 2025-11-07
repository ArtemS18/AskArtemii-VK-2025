from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete, insert, select, update, and_, func
from app.lib.log import log_call
from app.models import QuestionTagsORM
from sqlalchemy.orm import joinedload, selectinload
from app.models import QuestionORM, QuestionLikeORM, TagORM
from app.models.answers import AnswerORM
from app.models.users import UserORM, UserProfileORM

questions_options = (joinedload(QuestionORM.author).joinedload( UserORM.profile), 
                     joinedload(QuestionORM.tags), 
                     joinedload(QuestionORM.answers))
@log_call
async def get_questions_order_by_datetime(session: AsyncSession, limit: int = 10, offset: int =0) -> list[QuestionORM]:
    query = select(QuestionORM).order_by(QuestionORM.created_at.desc()).options(
        *questions_options
    )
    query = query.limit(limit).offset(offset)

    raw = await session.execute(query)
    questions = raw.scalars().unique().all()
    print(questions)
    return list(questions)
@log_call
async def get_questions_order_by_hots(session: AsyncSession, limit: int = 10, offset: int =0) -> list[QuestionORM]:
    query = select(QuestionORM).order_by(QuestionORM.likes_count.desc()).options(
        *questions_options
    )
    query = query.limit(limit).offset(offset)

    raw = await session.execute(query)
    questions = raw.scalars().unique().all()
    return list(questions)
@log_call
async def create_question_like(session: AsyncSession, user_id: int, question_id: int):
    query_insert = insert(QuestionLikeORM).values(user_id=user_id, question_id=question_id)
    query_update = update(QuestionORM).where(QuestionORM.id==question_id).values(likes_count=QuestionORM.likes_count+1)

    async with session.begin() as tr:
        await tr.session.execute(query_insert)
        await tr.session.execute(query_update)
@log_call
async def delete_question_like(session: AsyncSession, user_id: int, question_id: int):
    query_delete = delete(QuestionLikeORM).where(
        and_(QuestionLikeORM.user_id==user_id, QuestionLikeORM.question_id==question_id) 
    ).returning(QuestionLikeORM.question_id)
    query_update = update(QuestionORM).where(
        QuestionORM.id==question_id
    ).values(likes_count=QuestionORM.likes_count-1).returning(QuestionORM.id)

    async with session.begin() as tr:
        res = await tr.session.execute(query_delete)
        if res.scalar_one_or_none():
            res = await tr.session.execute(query_update)
            if not res.scalar_one_or_none():
                await tr.rollback()
            return 
        else:
            raise NoResultFound()
@log_call
async def get_question_by_id(session: AsyncSession, question_id: int) -> QuestionORM:
    query = select(QuestionORM).where(QuestionORM.id == question_id).options(
            joinedload(QuestionORM.author).joinedload( UserORM.profile), 
            joinedload(QuestionORM.tags), 
            joinedload(QuestionORM.answers).joinedload(AnswerORM.author).joinedload( UserORM.profile)
    )
    # query = select(QuestionORM).where(QuestionORM.id == question_id).options(
    #         selectinload(QuestionORM.author).selectinload( UserORM.profile), 
    #         selectinload(QuestionORM.tags), 
    #         selectinload(QuestionORM.answers).selectinload(AnswerORM.author).selectinload( UserORM.profile)
    # )
    raw = await session.execute(query)
    question = raw.scalars().unique().one_or_none()
    return question
@log_call
async def get_questions_by_tag(session: AsyncSession, tag_id: int, limit: int = 10, offset: int =0) -> list[QuestionORM]:
    query = (
        select(QuestionORM)
        .join(QuestionTagsORM, QuestionORM.id == QuestionTagsORM.question_id)
        .join(TagORM, QuestionTagsORM.tag_id == TagORM.id)
        .where(TagORM.id == tag_id)
        .options(*questions_options)
        )
    raw = await session.execute(query)
    questions = raw.scalars().unique().all()
    return list(questions)

async def get_questions_count(session: AsyncSession, tag_id: int | None = None) -> int:
    query = select(func.count(QuestionORM.id.distinct()))
    if tag_id is not None:
        query = (
            query.join(QuestionTagsORM, QuestionORM.id==QuestionTagsORM.question_id)
            .join(TagORM, QuestionTagsORM.tag_id == TagORM.id)
            .where(TagORM.id == tag_id)
        )
    raw = await session.execute(query)
    return raw.scalar_one()


async def get_tags_order_by_popular(session: AsyncSession, limit=10) -> list[TagORM]:
    query = select(TagORM).order_by(TagORM.popular_count.desc()).limit(limit)
    raw = await session.execute(query)
    questions = raw.scalars().all()
    return questions

async def get_users_order_by_popular(session: AsyncSession, limit=10) -> list[UserORM]:
    query = select(UserORM).order_by(UserORM.popular_count.desc()).limit(limit)
    raw = await session.execute(query)
    users = raw.scalars().all()
    return users
