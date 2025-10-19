from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.lib import templating
from app.web.templating import templates

router = APIRouter(prefix="")

@router.get("/ask", response_class=HTMLResponse)
async def get_ask_page(request: Request):
    base = await templating.get_base_page_values()
    return templates.TemplateResponse(request, "ask.html", context={**base})

@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@router.get("/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse(request, "signup.html")

