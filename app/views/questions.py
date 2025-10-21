from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import config
from app.lib import templating
from app.repository import crud

router = APIRouter(prefix="")
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


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
