from typing import Annotated
from fastapi import APIRouter, Body, Depends
from app.schemas.grade import GradeIn, GradeOut
from app.schemas.user import UserSession
from app.views.grade import GredeView
from sqlalchemy.exc import IntegrityError
from app.handlers.deps import StoreDep, csrf_validate, get_current_user

router = APIRouter(prefix="/grade", dependencies=[Depends(get_current_user), Depends(csrf_validate)])


@router.post("/like")
async def grade_handler(
    grade: Annotated[GradeIn,Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.create_question_grade(grade, user.id)
    return grade_count
    

@router.delete("/like")
async def grade_del_handler(
    grade: Annotated[GradeIn,Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.delete_question_grede(grade, user.id)
    return grade_count
    

@router.put("/like")
async def grade_put_handler(
    grade: Annotated[GradeIn,Body(embed=False)], 
    store: StoreDep, 
    user: UserSession= Depends(get_current_user)
) -> GradeOut:
    view = GredeView(store)
    grade_count =  await view.update_question_grade(grade, user.id)
    return grade_count
    