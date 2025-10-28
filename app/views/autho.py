from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.web.templating import template_response_base

router = APIRouter(prefix="")

@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    template = await template_response_base(request, "login.html", {})
    return template

@router.get("/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    template = await template_response_base(request, "signup.html", {})
    return template

