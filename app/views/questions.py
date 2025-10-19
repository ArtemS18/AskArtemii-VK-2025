from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from app.lib import utils
from app.web.templating import template_response_base
from app.repository import crud

router = APIRouter(prefix="")

@router.get("/", response_class=HTMLResponse)
async def question_view(request: Request):
    questions = await crud.mock_get_questions()
    base = await templating.get_base_page_values()
    return templates.TemplateResponse(request, "index.html", context={
        **base,
        "questions": questions
    })

@router.get("/questions/{id}", response_class=HTMLResponse)
async def ask_view(request: Request, id: int):
    questions = await crud.mock_get_questions()
    base = await templating.get_base_page_values()
    return templates.TemplateResponse(request, "question.html", context={
        **base,
        "question": questions[id],
    })
