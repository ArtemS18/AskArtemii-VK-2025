from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import HTMLResponse
from app.core.config import api_path
from app.handlers.deps import QuestionViewDep, get_current_user
from fastapi import Form

from app.models.users import UserORM
from app.schemas.user import User

router = APIRouter(prefix="")

@router.get(api_path.base, response_class=HTMLResponse)
async def questions_list_handler(
    view: QuestionViewDep,
    page: int = Query(default=1, ge=1)
):
    template = await view.questions_list_view(page)
    return template

@router.get(f"{api_path.question}/{{id}}", response_class=HTMLResponse)
async def question_handler(
    view: QuestionViewDep,
    id: int, 
    page: int = Query(default=1, ge=1)
):
    template = await view.question_view(id, page)
    return template


@router.get(api_path.hot, response_class=HTMLResponse)
async def questions_list_hots_handler(
    view: QuestionViewDep,
    page: int = Query(default=1, ge=1)
):
    template = await view.questions_list_hots_view(page)
    return template

@router.get(f"{api_path.tags}/{{tag_id}}", response_class=HTMLResponse)
async def questions_list_tags_view(
    view: QuestionViewDep,
    tag_id: int = Path(..., ge=0), 
    page: int = Query(default=1, ge=1)
):
    template = await view.questions_list_tags_view(tag_id, page)
    return template


@router.get(api_path.ask, response_class=HTMLResponse)
async def get_ask_page(view: QuestionViewDep, user: User = Depends(get_current_user)):
    template = await view.get_ask_page()
    return template


@router.post(api_path.ask)
async def post_ask_page(
    view: QuestionViewDep, 
    title: str = Form(...), 
    body: str = Form(...), 
    tags: str | None = Form(None), 
    user: User = Depends(get_current_user)
):
    return await view.create_question(title, body, user.id, tags)


@router.post(f"{api_path.question}/{{id}}/answer")
async def post_answer(
    view: QuestionViewDep, 
    id: int = Path(...), 
    answer: str = Form(...),
    user: User = Depends(get_current_user)
):
    return await view.create_answer(id, answer, user.id)