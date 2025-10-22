from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from app.lib import utils
from app.web.templating import template_response_base
from app.repository import crud

router = APIRouter(prefix="")

@router.get("/", response_class=HTMLResponse)
async def get_question_page(request: Request, page: int = Query(default=1, ge=1)):
    questions = await crud.mock_get_questions()

    pagination_data = utils.paginate(questions, request, per_page=5)

    template = await template_response_base(request, "index.html", {
        "pagination": pagination_data,
        "questions":pagination_data.items
        })
    return template

@router.get("/questions/{id}", response_class=HTMLResponse)
async def get_ask_page(request: Request, id: int, page: int = Query(default=1, ge=1)):
    questions = await crud.mock_get_questions()
    question = questions[id]
    pagination_data = utils.paginate(question.answers, request, per_page=5)
    template = await template_response_base(request, "question.html", {
        "question":question, 
        "answers": pagination_data.items,
        "pagination": pagination_data
        })
    return template

