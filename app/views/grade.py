from logging import getLogger
from typing import Any, Callable, Coroutine, TypeVar
import fastapi
from sqlalchemy import exc as sqlalchemy_exc
from app.schemas.grade import AnswerCorrect, AnswerGradeIn, AnswerOut, GradeIn, GradeOut
from app.repository import Store


_async_function = TypeVar("AsyncFunction", bound=Callable[..., Coroutine[Any, Any, Any]])
log = getLogger(__name__)

def _exeptions(func: _async_function) -> _async_function:
    async def wrapper(*args, **kwargs):
        try: 
            res = await func(*args, **kwargs)
            return res
        except sqlalchemy_exc.SQLAlchemyError as e:
            error_type = type(e)
            match error_type:
                case sqlalchemy_exc.IntegrityError:
                    log.error(e, exc_info=True)
                    raise fastapi.exceptions.HTTPException(status_code=409, detail="Item already existed")
                case _:
                    log.error(e, exc_info=True)
                    raise fastapi.exceptions.HTTPException(status_code=400, detail="Invalid data (in reall is db problem)")
    
    return wrapper


class GredeView:
    def __init__(self,  store: Store):
        self.store = store

    @_exeptions
    async def create_question_grade(self, grade: GradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.create_question_grade(user_id, grade.question_id, is_like=grade.is_like)
        return new_grade
        

    @_exeptions
    async def delete_question_grede(self, grade: GradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.delete_question_grade(user_id, grade.question_id)
        return new_grade
        

    @_exeptions
    async def update_question_grade(self, grade: GradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.update_question_grade(user_id, grade.question_id, grade.is_like)
        return new_grade
        

    @_exeptions
    async def create_answer_grade(self, grade: AnswerGradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.create_answer_grade(user_id, grade.answer_id, is_like=grade.is_like)
        return new_grade
        

    @_exeptions
    async def delete_answer_grede(self, grade: AnswerGradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.delete_answer_grade(user_id, grade.answer_id)
        return new_grade
        

    @_exeptions
    async def update_answer_grade(self, grade: AnswerGradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.update_answer_grade(user_id, grade.answer_id, grade.is_like)
        return new_grade
    
    @_exeptions
    async def correct_answer(self, grade: AnswerCorrect) -> AnswerOut:
        new_grade = await self.store.grade.correct_answer(grade.answer_id, grade.is_correct)
        return new_grade
        
