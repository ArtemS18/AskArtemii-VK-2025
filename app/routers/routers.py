from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="")
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse(request, "index.html")

@router.get("/question", response_class=HTMLResponse)
async def get_question_page(request: Request):
    return templates.TemplateResponse(request, "question.html")

@router.get("/ask", response_class=HTMLResponse)
async def get_ask_page(request: Request):
    return templates.TemplateResponse(request, "ask.html")

@router.get("/user", response_class=HTMLResponse)
async def get_user_page(request: Request):
    return templates.TemplateResponse(request, "user.html")

@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@router.get("/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse(request, "signup.html")

