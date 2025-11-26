from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.core.config import api_path
from app.handlers.deps import AuthoViewDep
from app.schemas.user import UserForm
from fastapi import Form
from typing import Optional

from fastapi import Request

router = APIRouter(prefix="")

@router.get(api_path.login, response_class=HTMLResponse)
async def login_view(view: AuthoViewDep):
    template = await view.login()
    return template

@router.post(api_path.login)
async def login_post_view(
    view: AuthoViewDep,
    email: str = Form(...),
    password: str = Form(...),
    continue_url: Optional[str] = Form(None)
):
    return await view.login_post(email, password, continue_url)

@router.get(api_path.singup, response_class=HTMLResponse)
async def signup_get(view: AuthoViewDep):
    return await view.template_response("signup.html")

@router.post(api_path.singup)
async def signup_view(
    view: AuthoViewDep,
    form: UserForm = Form(...)
):
    return await view.signup(form)

@router.get("/logout")
async def logout_view(view: AuthoViewDep, request: Request):
    return await view.logout()
