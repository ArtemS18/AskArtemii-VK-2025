from fastapi import APIRouter, Path, Query, Request
from fastapi.responses import HTMLResponse
from app.core.config import config
from app.deps import SessionDep
from app.lib import utils
from app.web.templating import template_response_base
from app.repository import mock_crud
from app.repository import crud

router = APIRouter(prefix="")
api = config.endpoint
PER_PAGE = 10

@router.get(api.base, response_class=HTMLResponse)
async def questions_list_view(
    request: Request, 
    session: SessionDep, 
    page: int = Query(default=1, ge=1)
):
    total = await crud.get_questions_count(session)
    offset = utils.get_offset(total, page, PER_PAGE)
    questions = await crud.get_questions_order_by_datetime(session, limit=PER_PAGE, offset=offset)
    pagination_data = utils.paginate(total, request, PER_PAGE)

    template = await template_response_base(request, "index.html", {
        "pagination": pagination_data,
        "questions":questions
        })
    return template

@router.get(api.question + "/{id}", response_class=HTMLResponse)
async def question_view(
    request: Request, 
    id: int, 
    session: SessionDep, 
    page: int = Query(default=1, ge=1)
):
    question = await crud.get_question_by_id(session, id)
    pagination_data = utils.paginate(question.answers_count, request, PER_PAGE)
    template = await template_response_base(
        request, "question.html", {
            "question":question, 
            "answers": question.answers,
            "pagination": pagination_data
            }
        )
    return template

@router.get(api.hot, response_class=HTMLResponse)
async def questions_list_hots_view(
    request: Request,
    session: SessionDep,
    page: int = Query(default=1, ge=1)
):
    total = await crud.get_questions_count(session)
    offset = utils.get_offset(total, page, PER_PAGE)
    questions = await crud.get_questions_order_by_hots(session, limit=PER_PAGE, offset=offset)
    pagination_data = utils.paginate(total, request, PER_PAGE)

    template = await template_response_base(
        request, "hot_questions.html", {
            "pagination": pagination_data,
            "questions":questions
            }
    )
    return template

@router.get(api.tags+"/{tag_id}", response_class=HTMLResponse)
async def questions_list_tags_view(
    request: Request, 
    session: SessionDep,
    tag_id: int = Path(..., ge=0), 
    page: int = Query(default=1, ge=1)
):
    total = await crud.get_questions_count(session, tag_id=tag_id)
    offset = utils.get_offset(total, page, PER_PAGE)
    questions = await crud.get_questions_by_tag(session, tag_id=tag_id, limit=PER_PAGE, offset=offset)
    pagination_data = utils.paginate(total, request, PER_PAGE)

    template = await template_response_base(
        request, "hot_questions.html", {
            "pagination": pagination_data,
            "questions":questions
            }
    )
    return template


@router.get(api.ask, response_class=HTMLResponse)
async def get_ask_page(request: Request):
    template = await template_response_base(request, "ask.html", {})
    return template