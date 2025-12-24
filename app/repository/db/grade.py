from typing import Any
from sqlalchemy import and_, delete, insert, select, update
from app.lib.log import log_call
from app.models.answers import AnswerORM
from app.models.base import BaseORM
from app.models.grade import AnswerGradeORM, QuestionGradeORM
from app.models.questions import QuestionORM
from app.repository.db.client import PostgresClient

from app.schemas.grade import AnswerOut, GradeOut

class GradesRepo:
    mm_model: BaseORM
    

    def __init__(self, pg: PostgresClient):
        self.pg = pg

    async def _insert_and_update(self,  query_insert, query_update) -> dict[str, Any]:
        async with self.pg.get_session() as session:
            try:
                await session.execute(query_insert)
                raw = await session.execute(query_update)
                grade_dict = raw.mappings().one_or_none()
                if not grade_dict:
                    await session.rollback()
                    return False
                await session.commit()
                return grade_dict
            except Exception as e:
                await session.rollback()
                raise e

        
    @log_call
    async def create_question_grade(self, user_id: int, question_id: int, is_like: bool) -> GradeOut:
        query_insert = insert(QuestionGradeORM).values(user_id=user_id, question_id=question_id, is_like=is_like)
        
        _query_update = update(QuestionORM).where(QuestionORM.id==question_id)
        _query_update = _query_update.values(like_count=QuestionORM.like_count+1) if is_like else _query_update.values(dislike_count=QuestionORM.dislike_count+1)
        query_update = _query_update.returning(QuestionORM.like_count, QuestionORM.dislike_count)

        res = await self._insert_and_update(query_insert, query_update)
        return GradeOut(**res)
        
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

        res = await self._insert_and_update(query_insert, query_update)
        return GradeOut(**res)


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
            
    @log_call
    async def create_answer_grade(self, user_id: int, answer_id: int, is_like: bool) -> GradeOut:
        query_insert = insert(AnswerGradeORM).values(user_id=user_id, answer_id=answer_id, is_like=is_like)
        
        _update = update(AnswerORM).where(AnswerORM.id==answer_id)
        query_update = _update.values(like_count=AnswerORM.like_count+1) if is_like else _update.values(dislike_count=AnswerORM.dislike_count+1)
        query_update=query_update.returning(AnswerORM.like_count, AnswerORM.dislike_count)

        res = await self._insert_and_update(query_insert, query_update)
        return GradeOut(**res)
        
    @log_call
    async def update_answer_grade(self, user_id: int, answer_id: int, is_like: bool) -> GradeOut:
        query_insert = update(AnswerGradeORM).where(and_(AnswerGradeORM.user_id == user_id, AnswerGradeORM.answer_id == answer_id)).values(is_like=is_like)
        
        _update = update(AnswerORM).where(AnswerORM.id==answer_id)
        query_update = (
            _update
            .values(
                like_count=AnswerORM.like_count+1, 
                dislike_count=AnswerORM.dislike_count-1
            ) if is_like else _update.values(
                like_count=AnswerORM.like_count-1, 
                dislike_count=AnswerORM.dislike_count+1
            )
        )
        query_update=query_update.returning(AnswerORM.like_count, AnswerORM.dislike_count)

        res = await self._insert_and_update(query_insert, query_update)
        return GradeOut(**res)


    @log_call
    async def delete_answer_grade(self, user_id: int, answer_id: int)-> GradeOut:
        query_delete = delete(AnswerGradeORM).where(
            and_(AnswerGradeORM.user_id==user_id, AnswerGradeORM.answer_id==answer_id) 
        ).returning(AnswerGradeORM)
        query_update = update(AnswerORM).where(AnswerORM.id==answer_id)


        async with self.pg.get_session() as session:
            try:
                raw = await session.execute(query_delete)
                grade = raw.scalar_one_or_none()
                if grade is None:
                    await session.rollback()
                    return
                query_update=query_update.values(like_count=AnswerORM.like_count-1) if grade.is_like else query_update.values(dislike_count=AnswerORM.dislike_count-1)
                query_update=query_update.returning(AnswerORM.like_count, AnswerORM.dislike_count)
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
            
    @log_call
    async def set_correct_answer(self, answer_id: int, is_correct_: bool) -> AnswerOut:
        query_update = update(AnswerORM).where(AnswerORM.id==answer_id).values(is_correct=is_correct_).returning(AnswerORM.id, AnswerORM.is_correct)
        res = await self.pg.mapping(query_update)
        return AnswerOut.model_validate(res, by_alias=True)
    
    @log_call
    async def del_correct_answers(self, answer_id: int):
        _sub_query = select(AnswerORM.question_id).where(AnswerORM.id==answer_id).limit(1).subquery()
        query_update = update(AnswerORM).where(and_(AnswerORM.question_id==_sub_query, AnswerORM.id != answer_id)).values(is_correct=False)
        await self.pg._execute(query_update)
    
