from logging import getLogger
from typing import Any, Union
from uuid import UUID
import uuid
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates

from app.core.config import config, api_path
from app.lib.log import log_call
from app.lib.random_ import get_random_seq
from app.repository import Store
from app.schemas.user import UserSession

log = getLogger(__name__)

class BaseView():
    def __init__(self, request: Request, store: Store):
        self.request = request
        self.store = store
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
    
    async def _get_session(self) -> UserSession:
        key = self.request.cookies.get("session")
        if key is not None:
            user_session = await self.store.redis.get_session(key)
            return user_session
        
    async def _get_user_id(self) -> int | None:
        session = await self._get_session()
        if session is not None:
            return session.id
    
    async def _set_session(self, resp: Response, id_: int, nickname: str, img_url: str):
        session_key = get_random_seq()
        csrf_token = uuid.uuid4()
        await self.store.redis.create_user_session(session_key, UserSession(id=id_, nickname=nickname,img_url=img_url, csrf_token=csrf_token))
        resp.set_cookie("session", session_key, httponly=True)
        return session_key

    async def _get_layout_data(self) -> dict[str, Any]:
        best_users = await self.store.user.get_users_order_by_popular()
        popular_tags = await self.store.tag.get_tags_order_by_popular()
        user_session: UserSession | None = None
        csrf_token: UUID | None = None
        key = self.request.cookies.get("session")
        if key is not None:
            user_session = await self.store.redis.get_session(key)
            if user_session:
                csrf_token = user_session.csrf_token
        return {
            "best_users": best_users, 
            "popular_tags": popular_tags ,
            "user_profile": user_session,

            "URL_HOME": api_path.base,
            "URL_ASK": api_path.ask,
            "URL_QUESTION": api_path.question,
            "URL_LOGIN": api_path.login,
            "URL_SIGNUP": api_path.singup,
            "URL_USER": api_path.user,
            "URL_HOT_QUESTION": api_path.hot,
            "URL_HOT_TAGS": api_path.tags,
            "CSRF_TOKEN": csrf_token,
            "STATIC_URL": f"{config.local_storage_url}/static",
            "CENTRIFUGO_WS_URL": "ws://localhost:8090/connection/websocket",
            "CENTRIFUGO_TOKEN_URL": "/centrifugo/token",

        }

