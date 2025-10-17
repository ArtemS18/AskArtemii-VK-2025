from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import config
from app.lib import templating

router = APIRouter(prefix="")
templates = Jinja2Templates(directory=config.TEMPLATE_PATH)


@router.get("/ask", response_class=HTMLResponse)
async def get_ask_page(request: Request):
    base = await templating.get_base_page_values()
    return templates.TemplateResponse(request, "ask.html", context={**base})

@router.get("/user", response_class=HTMLResponse)
async def get_user_page(request: Request):
    return templates.TemplateResponse(request, "user.html")

@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@router.get("/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse(request, "signup.html")

