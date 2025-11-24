from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.core.config import config
from app.handlers.deps import AuthoViewDep

router = APIRouter(prefix="")
api = config.endpoint

@router.get(api.login, response_class=HTMLResponse)
async def login_view(view: AuthoViewDep):
    template = await view.login()
    return template

@router.get(api.singup, response_class=HTMLResponse)
async def signup_view(view: AuthoViewDep):
    template = await view.signup()
    return template

