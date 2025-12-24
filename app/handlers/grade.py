from typing import Annotated
from fastapi import APIRouter, Body, Depends
from app.schemas.grade import AnswerCorrect, AnswerGradeIn, AnswerOut, GradeIn, GradeOut
from app.schemas.user import UserSession
from app.views.grade import GredeView
from app.handlers.deps import StoreDep, csrf_validate, get_current_user, validate_author_answer

router = APIRouter(prefix="/grade", dependencies=[Depends(get_current_user), Depends(csrf_validate)])


@router.post("/like")
async def grade_handler(
    grade: Annotated[GradeIn, Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.create_question_grade(grade, user.id)
    return grade_count
    

@router.delete("/like")
async def grade_del_handler(
    grade: Annotated[GradeIn, Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.delete_question_grede(grade, user.id)
    return grade_count
    

@router.put("/like")
async def grade_put_handler(
    grade: Annotated[GradeIn, Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.update_question_grade(grade, user.id)
    return grade_count
    
@router.post("/answer")
async def answer_grade_handler(
    grade: Annotated[AnswerGradeIn, Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.create_answer_grade(grade, user.id)
    return grade_count
    

@router.delete("/answer")
async def answer_grade_del_handler(
    grade: Annotated[AnswerGradeIn, Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.delete_answer_grede(grade, user.id)
    return grade_count
    

@router.put("/answer")
async def answer_grade_put_handler(
    grade: Annotated[AnswerGradeIn, Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.update_answer_grade(grade, user.id)
    return grade_count
    
@router.patch("/answer/correct", dependencies=[Depends(validate_author_answer)])
async def answer_correct_handler(
    grade: Annotated[AnswerCorrect, Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> AnswerOut:
    view = GredeView(store)
    grade_count =  await view.correct_answer(grade, user.id)
    return grade_count