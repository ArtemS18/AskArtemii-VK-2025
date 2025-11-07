
from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.core.config import config
from app.repository import mock_crud


templates = Jinja2Templates(directory=config.template_path)

async def template_response_base(request: Request, template_name: str, context: dict[str, Any] = {}):
    base_val = await get_base_page_values()
    return templates.TemplateResponse(request, template_name, context={**base_val, **context})



async def get_base_page_values() -> dict[str, Any]:
    
    best_users = await mock_crud.mock_get_users()
    popular_tags = await mock_crud.mock_get_tags()
    user = await mock_crud.mock_get_users()
    return {
        "best_users": best_users, 
        "popular_tags": popular_tags ,
        "user": user[0],
        }

templates.env.globals.update({
    "URL_HOME": config.endpoint.base,
    "URL_ASK": config.endpoint.ask,
    "URL_QUESTION": config.endpoint.question,
    "URL_LOGIN": config.endpoint.login,
    "URL_SIGNUP": config.endpoint.singup,
    "URL_USER": config.endpoint.user,
    "URL_HOT_QUESTION": config.endpoint.hot,
    "URL_HOT_TAGS": config.endpoint.tags,
})