from fastapi import APIRouter, Path, Query
from fastapi.responses import HTMLResponse
from app.core.config import config
from app.handlers.deps import QuestionViewDep

router = APIRouter(prefix="")
api = config.endpoint

@router.get(api.base, response_class=HTMLResponse)
async def questions_list_handler(
    view: QuestionViewDep,
    page: int = Query(default=1, ge=1)
):
    template = await view.questions_list_view(page)
    return template

@router.get(api.question + "/{id}", response_class=HTMLResponse)
async def question_handler(
    view: QuestionViewDep,
    id: int, 
    page: int = Query(default=1, ge=1)
):
    template = await view.question_view(id, page)
    return template


@router.get(api.hot, response_class=HTMLResponse)
async def questions_list_hots_handler(
    view: QuestionViewDep,
    page: int = Query(default=1, ge=1)
):
    template = await view.questions_list_hots_view(page)
    return template

@router.get(api.tags+"/{tag_id}", response_class=HTMLResponse)
async def questions_list_tags_view(
    view: QuestionViewDep,
    tag_id: int = Path(..., ge=0), 
    page: int = Query(default=1, ge=1)
):
    template = await view.questions_list_tags_view(tag_id, page)
    return template


@router.get(api.ask, response_class=HTMLResponse)
async def get_ask_page( view: QuestionViewDep,):
    template = await view.get_ask_page()
    return template