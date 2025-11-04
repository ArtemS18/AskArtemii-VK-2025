from fastapi import APIRouter, Path, Query, Request
from fastapi.responses import HTMLResponse
from app.core.config import config
from app.lib import utils
from app.web.templating import template_response_base
from app.repository import crud

router = APIRouter(prefix="")
api = config.endpoint

@router.get(api.base, response_class=HTMLResponse)
async def questions_list_view(request: Request, page: int = Query(default=1, ge=1)):
    questions = await crud.mock_get_questions()

    pagination_data = utils.paginate(questions, request, per_page=5)

    template = await template_response_base(request, "index.html", {
        "pagination": pagination_data,
        "questions":pagination_data.items
        })
    return template

@router.get(api.question + "/{id}", response_class=HTMLResponse)
async def question_view(request: Request, id: int, page: int = Query(default=1, ge=1)):
    questions = await crud.mock_get_questions()
    question = questions[id]
    pagination_data = utils.paginate(question.answers, request, per_page=5)
    template = await template_response_base(request, "question.html", {
        "question":question, 
        "answers": pagination_data.items,
        "pagination": pagination_data
        })
    return template

@router.get(api.hot, response_class=HTMLResponse)
async def questions_list_hots_view(request: Request, page: int = Query(default=1, ge=1)):
    questions = await crud.mock_get_questions()

    pagination_data = utils.paginate(questions, request, per_page=5)

    template = await template_response_base(request, "hot_questions.html", {
        "pagination": pagination_data,
        "questions":pagination_data.items
        })
    return template

@router.get(api.tags+"/{tag_id}", response_class=HTMLResponse)
async def questions_list_tags_view(request: Request, tag_id: int = Path(..., ge=0), page: int = Query(default=1, ge=1)):
    questions = await crud.mock_get_questions_by_tag(tag_id)
    tag = await crud.mock_get_tags()
    pagination_data = utils.paginate(questions, request, per_page=5)
    template = await template_response_base(request, "tags_questions.html", {
        "tag": tag[tag_id],
        "pagination": pagination_data,
        "questions":pagination_data.items
        })
    return template


@router.get(api.ask, response_class=HTMLResponse)
async def get_ask_page(request: Request):
    template = await template_response_base(request, "ask.html", {})
    return template