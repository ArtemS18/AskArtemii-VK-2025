from pydantic import BaseModel


class GradeIn(BaseModel):
    question_id: int 
    is_like: bool 

class GradeOut(BaseModel):
    like_count: int 
    dislike_count: int
