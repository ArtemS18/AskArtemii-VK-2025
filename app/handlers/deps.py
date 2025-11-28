from typing import Annotated
from fastapi import Cookie, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import config
from app.repository.minio.avatars import UserAvatarRepository
from app.schemas.user import User
from app.views.questions import QuestionView
from app.views.autho import AuthoView
from urllib.parse import quote
from app.views.users import UserView
from app.core.db import SessionLocal
from app.repository.redis import sessions

async def get_db():
    async with SessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_minio():
    return UserAvatarRepository(
        config.minio.url, 
        config.minio.access_key, 
        config.minio.secret_key
    )
UserAvatarDep = Annotated[QuestionView, Depends(get_minio)]

async def get_question_view(req: Request, session: SessionDep):
    return QuestionView(session, req)

QuestionViewDep = Annotated[QuestionView, Depends(get_question_view)]

async def get_autho_view(req: Request, session: SessionDep):
    return AuthoView(session, req)

AuthoViewDep = Annotated[AuthoView, Depends(get_autho_view)]

async def get_users_view(req: Request, session: SessionDep, minio: UserAvatarDep):
    return UserView(session, req, minio)

UserViewDep = Annotated[UserView, Depends(get_users_view)]


async def get_current_user(req: Request) -> User | None:
    user_session= req.cookies.get("session")
    
    dest = req.url.path
    if req.url.query:
        dest = f"{dest}?{req.url.query}"

    dest_q = quote(dest, safe="")
    location = f"{config.endpoint.login}?continue_url={dest_q}"
    exp = HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={
            "Location": location
        })
    
    if not user_session:
        raise exp
    
    user = await sessions.get_session(user_session)

    if not user:
        raise exp
    
    return user