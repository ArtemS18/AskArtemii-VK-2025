from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.config import config
from app.entities.error import ErrorTemplate
from app.web.templating import template_response_base

api = config.endpoint

router = APIRouter(prefix=api.user)

@router.get("/me", response_class=HTMLResponse)
async def user_settings_view(request: Request):
    template = await template_response_base(request, "user.html")
    return template
