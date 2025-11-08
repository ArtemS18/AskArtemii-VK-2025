from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.views.questions import QuestionView
from app.views.autho import AuthoView
from app.views.users import UserView
from app.core.db import SessionLocal

async def get_db():
    async with SessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]

async def get_question_view(req: Request, session: SessionDep):
    return QuestionView(session, req)

QuestionViewDep = Annotated[QuestionView, Depends(get_question_view)]

async def get_autho_view(req: Request, session: SessionDep):
    return AuthoView(session, req)

AuthoViewDep = Annotated[AuthoView, Depends(get_autho_view)]

async def get_users_view(req: Request, session: SessionDep):
    return UserView(session, req)

UserViewDep = Annotated[UserView, Depends(get_users_view)]