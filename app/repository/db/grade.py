from sqlalchemy import and_, delete, insert, update
from app.lib.log import log_call
from app.models.grade import QuestionGradeORM
from app.models.questions import QuestionORM
from app.repository.db.client import PostgresClient

from app.schemas.grade import GradeOut

class GradesRepo:

    def __init__(self, pg: PostgresClient):
        self.pg = pg

        
    @log_call
    async def create_question_grade(self, user_id: int, question_id: int, is_like: bool) -> GradeOut:
        query_insert = insert(QuestionGradeORM).values(user_id=user_id, question_id=question_id, is_like=is_like)
        
        _update = update(QuestionORM).where(QuestionORM.id==question_id)
        query_update = _update.values(like_count=QuestionORM.like_count+1) if is_like else _update.values(dislike_count=QuestionORM.dislike_count+1)
        query_update=query_update.returning(QuestionORM.like_count, QuestionORM.dislike_count)

        async with self.pg.get_session() as session:
            try:
                await session.execute(query_insert)
                raw = await session.execute(query_update)
                grade_dict = raw.mappings().one_or_none()
                if not grade_dict:
                    await session.rollback()
                    return False
                await session.commit()
                return GradeOut(**grade_dict)
            except Exception as e:
                await session.rollback()
                raise e
        
    @log_call
    async def update_question_grade(self, user_id: int, question_id: int, is_like: bool) -> GradeOut:
        query_insert = update(QuestionGradeORM).where(and_(QuestionGradeORM.user_id == user_id, QuestionGradeORM.question_id == question_id)).values(is_like=is_like)
        
        _update = update(QuestionORM).where(QuestionORM.id==question_id)
        query_update = (
            _update
            .values(
                like_count=QuestionORM.like_count+1, 
                dislike_count=QuestionORM.dislike_count-1
            ) if is_like else _update.values(
                like_count=QuestionORM.like_count-1, 
                dislike_count=QuestionORM.dislike_count+1
            )
        )
        query_update=query_update.returning(QuestionORM.like_count, QuestionORM.dislike_count)

        async with self.pg.get_session() as session:
            try:
                await session.execute(query_insert)
                raw = await session.execute(query_update)
                grade_dict = raw.mappings().one_or_none()
                if not grade_dict:
                    await session.rollback()
                    return False
                await session.commit()
                return GradeOut(**grade_dict)
            except Exception as e:
                await session.rollback()
                raise e


    @log_call
    async def delete_question_grade(self, user_id: int, question_id: int)-> GradeOut:
        query_delete = delete(QuestionGradeORM).where(
            and_(QuestionGradeORM.user_id==user_id, QuestionGradeORM.question_id==question_id) 
        ).returning(QuestionGradeORM)
        query_update = update(QuestionORM).where(QuestionORM.id==question_id)


        async with self.pg.get_session() as session:
            try:
                raw = await session.execute(query_delete)
                grade = raw.scalar_one_or_none()
                if grade is None:
                    await session.rollback()
                    return
                query_update=query_update.values(like_count=QuestionORM.like_count-1) if grade.is_like else query_update.values(dislike_count=QuestionORM.dislike_count-1)
                query_update=query_update.returning(QuestionORM.like_count, QuestionORM.dislike_count)
                raw = await session.execute(query_update)
                grade_dict = raw.mappings().one_or_none()
                if grade_dict is None:
                    await session.rollback()
                    return
                await session.commit()
                return GradeOut(**grade_dict)
            except Exception as e:
                    await session.rollback()
                    raise e