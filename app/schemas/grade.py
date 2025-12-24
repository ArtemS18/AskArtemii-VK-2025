from pydantic import BaseModel, ConfigDict, Field


class GradeIn(BaseModel):
    question_id: int 
    is_like: bool 

class AnswerGradeIn(BaseModel):
    answer_id: int 
    is_like: bool 
    question_id: int 

class AnswerCorrect(BaseModel):
    answer_id: int = Field(alias="id")
    is_correct: bool 
    question_id: int
    model_config = ConfigDict(
        populate_by_name=True,
    )


class GradeOut(BaseModel):
    like_count: int 
    dislike_count: int


class AnswerOut(BaseModel):
    answer_id: int = Field(alias="id")
    is_correct: bool 