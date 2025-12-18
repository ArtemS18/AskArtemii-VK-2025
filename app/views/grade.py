from app.schemas.grade import GradeIn, GradeOut
from app.repository import Store

class GredeView:
    def __init__(self,  store: Store):
        self.store = store

    async def create_question_grade(self, grade: GradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.create_question_grade(user_id, grade.question_id, is_like=grade.is_like)
        return new_grade
    
    async def delete_question_grede(self, grade: GradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.delete_question_grade(user_id, grade.question_id)
        return new_grade
    
    async def update_question_grade(self, grade: GradeIn, user_id: int) -> GradeOut:
        new_grade = await self.store.grade.update_question_grade(user_id, grade.question_id, grade.is_like)
        return new_grade
    