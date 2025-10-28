from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.config import config
from app.web.templating import template_response_base

router = APIRouter(prefix="")
api = config.endpoint

@router.get(api.login, response_class=HTMLResponse)
async def login_view(request: Request):
    template = await template_response_base(request, "login.html", {})
    return template

@router.get(api.singup, response_class=HTMLResponse)
async def signup_view(request: Request):
    template = await template_response_base(request, "signup.html", {})
    return template

