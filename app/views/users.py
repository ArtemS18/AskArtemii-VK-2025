from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.models.error import ErrorTemplate
from app.web.templating import template_response_base

router = APIRouter(prefix="/users")

@router.get("/me", response_class=HTMLResponse)
async def get_user_page(request: Request):
    template = await template_response_base(request, "user.html")
    return template
