from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from app.core.config import config
from app.repository import Store, get_store
from app.schemas.user import UserSession
from app.views.questions import QuestionView
from app.views.autho import AuthoView
from urllib.parse import quote
from app.views.users import UserView


StoreDep = Annotated[Store, Depends(get_store)]

async def get_question_view(req: Request, store: StoreDep):
    return QuestionView(req, store)


async def get_autho_view(req: Request, store: StoreDep):
    return AuthoView(req, store)

async def get_users_view(req: Request, store: StoreDep):
    return UserView(req, store)

async def get_current_user(req: Request,  store: StoreDep) -> UserSession :
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
    
    user = await store.redis.get_session(user_session)

    if not user:
        raise exp
    
    return user


AuthoViewDep = Annotated[AuthoView, Depends(get_autho_view)]
QuestionViewDep = Annotated[QuestionView, Depends(get_question_view)]
UserViewDep = Annotated[UserView, Depends(get_users_view)]
