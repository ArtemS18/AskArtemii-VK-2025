
from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.config.config import config
from app.repository import crud


templates = Jinja2Templates(directory=config.template.dir)

async def template_response_base(request: Request, template_name: str, context: dict[str, Any] = {}):
    base_val = await get_base_page_values()
    return templates.TemplateResponse(request, template_name, context={**base_val, **context})



async def get_base_page_values() -> dict[str, Any]:
    
    best_users = await crud.mock_get_users()
    popular_tags = await crud.mock_get_tags()
    user = await crud.mock_get_users()
    return {
        "best_users": best_users, 
        "popular_tags": popular_tags ,
        "user": user[0]
        }
