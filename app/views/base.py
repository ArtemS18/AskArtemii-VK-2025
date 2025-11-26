from logging import getLogger
from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config, api_path
from app.lib.log import log_call
from app.repository.db import user as crud
from app.repository.db import question
from app.repository.redis import sessions

log = getLogger(__name__)

class BaseView():
    def __init__(self, session: AsyncSession, request: Request):
        self.request = request
        self.session = session
        self.templates = Jinja2Templates(directory=config.template_path)

    @log_call
    async def template_response(self, template_name: str, context: dict[str, Any] = {}):
        layout_data = await self._get_layout_data()
        return self.templates.TemplateResponse(
            self.request, 
            template_name, 
            context={
                **layout_data, 
                **context
            }
        )
    async def template_paginate(self, template_name: str, context_: dict[str, Any] = {}):

        def url_with_page(page: int) -> str:
            return f"{self.request.url.path}?page={page}"
        
        context = context_.copy()
        context.update({
            "url_with_page": url_with_page
            }
        )
        return await self.template_response(template_name, context)
    
    async def get_user_id_from_cookie(self) -> int | None:
        uid = self.request.cookies.get("user_id")
        if not uid:
            return None
        try:
            uid_i = int(uid)
        except Exception:
            return None
        return uid_i

    async def _get_layout_data(self) -> dict[str, Any]:
        best_users = await question.get_users_order_by_popular()
        popular_tags = await question.get_tags_order_by_popular()
        user = None
        key = self.request.cookies.get("session")
        if key is not None:
            user = await sessions.get_session(key)
        return {
            "best_users": best_users, 
            "popular_tags": popular_tags ,
            "user_profile": user,

            "URL_HOME": api_path.base,
            "URL_ASK": api_path.ask,
            "URL_QUESTION": api_path.question,
            "URL_LOGIN": api_path.login,
            "URL_SIGNUP": api_path.singup,
            "URL_USER": api_path.user,
            "URL_HOT_QUESTION": api_path.hot,
            "URL_HOT_TAGS": api_path.tags,
            }

