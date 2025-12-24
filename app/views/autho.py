from typing import Optional

from fastapi import Request, Response, status
from fastapi.responses import RedirectResponse
from app.repository import Store
from app.schemas.error import ErrorTemplate
from app.schemas.user import UserSession, UserForm, UserWrite
from app.views.base import BaseView
from app.lib.random_ import get_random_seq
from app.core.config import api_path, BASE_IMG
from app.lib import password as pwd
import uuid


class AuthoView(BaseView):
    def __init__(self, request: Request, store: Store):
        super().__init__(request, store)

    async def login_page(self, **context):
        return await self.template_response("login.html", context)
    
    async def singup_page(self, **context):
        return await self.template_response("signup.html", context)

    async def login_post(self, email: str, password: str, continue_url: Optional[str] = None):
        user = await self.store.user.get_user_by_email(email)

        for k, v in {"email": email, "password": password}.items():
            if v is None or v == "":
                return await self.login_page(
                        email=email,
                        password=password, 
                        error=ErrorTemplate(text=f"Поле {k} должно быть заполнено")
                    )
                
        if not user:
            return await self.login_page(
                error=ErrorTemplate(text="Неправельний email или пароль"),
                email=email,
                password=password
            )

        if not pwd.verify_password(password, user.hashed_password):
           return await self.login_page(
                error=ErrorTemplate(text="Неправельний email или пароль"),
                email=email,
                password=password
            )

        dest = continue_url or api_path.base
        response = RedirectResponse(dest, status_code=status.HTTP_303_SEE_OTHER)
        await self._set_session(response,
            id_=user.id,
            nickname=user.profile.nickname,
            img_url=user.profile.img_url
        )

        return response

    async def signup_post(self, form_data: UserForm):
        context = form_data.model_dump()

        for k, v in context.items():
            if v is None or v == "":
                return await self.singup_page(**context, error=ErrorTemplate(text=f"Поле {k} должно быть заполнено"))
                
        if len(form_data.password) < 8:
            return await self.singup_page(**context, error=ErrorTemplate(text="Длина пароля должны быть минимум 8 символов"))
        
        if form_data.password != form_data.password_confirm:
            return await self.singup_page(**context, error=ErrorTemplate(text="Пароли не совпадают"))
        
        

        if await self.store.user.get_user_by_email(form_data.email):
            return await self.singup_page(**context, error=ErrorTemplate(text="Пользователь с таким email уже зарегистрирован"))

        pwd_hashed = pwd.hash_password(form_data.password)
        user_data = UserWrite(
            nickname=form_data.nickname,
            email=form_data.email, 
            hashed_password=pwd_hashed,
            img_url=BASE_IMG
            )

        user_orm = await self.store.user.create_user(user_data)

        response = RedirectResponse(api_path.base, status_code=303)
        await self._set_session(response,
            id_=user_orm.id,
            nickname=user_data.nickname,
            img_url=user_data.img_url
        )
        return response

    async def logout(self):
        response = RedirectResponse(api_path.login, status_code=303)
        self_id = self.request.cookies.get("session")
        if self_id:
            await self.store.redis.delete_session(self_id)
            response.delete_cookie("session")
        return response


