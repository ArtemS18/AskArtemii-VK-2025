from typing import Optional

from fastapi import Request, Response, status
from fastapi.responses import RedirectResponse
from app.schemas.error import ErrorTemplate
from app.schemas.user import User, UserForm, UserWrite
from app.views.base import BaseView
from app.repository.db import user as crud
from app.repository.redis import sessions
from app.lib.random_ import get_random_seq
from app.core.config import api_path, BASE_IMG
from app.lib import password as pwd
from sqlalchemy.ext.asyncio import AsyncSession


class AuthoView(BaseView):
    def __init__(self, session: AsyncSession, req: Request):
        super().__init__(session, req)

    async def login(self):
        return await self.template_response("login.html")
    
    async def _set_session(self, resp: Response, user: User):
        session_key = get_random_seq()
        await sessions.create_session(session_key, user)
        resp.set_cookie("session", session_key, httponly=True)
        return session_key

    async def login_post(self, email: str, password: str, continue_url: Optional[str] = None):
        user = await crud.get_user_by_email(self.session, email)
        context = {
            "email": email,
        }
        if not user:
              context["error"] =ErrorTemplate(text="Invalid email or password.")
              return await self.template_response("login.html", context)

        if not pwd.verify_password(password, user.hashed_password):
           context["error"] =ErrorTemplate(text="Invalid email or password.")
           return await self.template_response("login.html", context)

        dest = continue_url or api_path.base
        response = RedirectResponse(dest, status_code=status.HTTP_303_SEE_OTHER)
        await self._set_session(response, User(
            id=user.id,
            nickname=user.profile.nickname,
            email=user.email,
            img_url=user.profile.img_url
        ))

        return response

    async def signup(self, form_data: UserForm):
        context = form_data.model_dump()
        if form_data.password != form_data.password_confirm:
            context["error"] = ErrorTemplate(text="Passwords do not match.")
            return await self.template_response("signup.html", context)

        if await crud.get_user_by_email(self.session, form_data.email):
            context["error"] =  ErrorTemplate(text="User with this email already exists.")
            return await self.template_response("signup.html", context)

        pwd_hashed = pwd.hash_password(form_data.password)
        user_data = UserWrite(
            nickname=form_data.nickname,
            email=form_data.email, 
            hashed_password=pwd_hashed,
            img_url=BASE_IMG
            )

        user_orm = await crud.create_user(self.session, user_data)

        response = RedirectResponse(api_path.base, status_code=303)
        await self._set_session(response,  User(
            id=user_orm.id,
            nickname=user_data.nickname,
            email=user_data.email,
            img_url=user_data.img_url
        ))
        return response

    async def logout(self):
        response = RedirectResponse(api_path.login, status_code=303)
        self_id = self.request.cookies.get("session")
        if self_id:
            await sessions.delete_session(self_id)
            response.delete_cookie("session")
        return response


