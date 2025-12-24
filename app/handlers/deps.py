import json
from logging import getLogger
from typing import Annotated
from uuid import UUID
from fastapi import Body, Depends, Form, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from app.core.config import config
from app.repository import Store, get_store
from app.schemas.user import UserSession
from app.views.questions import QuestionView
from app.views.autho import AuthoView
from urllib.parse import quote
from app.views.users import UserView

log = getLogger(__name__)


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
    json_exeption =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    if not user_session:
        raise json_exeption
    
    user = await store.redis.get_session(user_session)

    if not user:
        raise json_exeption
    
    return user

async def get_existed_user(req: Request,  store: StoreDep) -> UserSession :
    user_session= req.cookies.get("session")
    
    if user_session:
        user = await store.redis.get_session(user_session)

        return user
    else:
        return None


AuthoViewDep = Annotated[AuthoView, Depends(get_autho_view)]
QuestionViewDep = Annotated[QuestionView, Depends(get_question_view)]
UserViewDep = Annotated[UserView, Depends(get_users_view)]

async def get_csrf_token(req: Request):
    csrf_token = req.headers.get('X-CSRFToken')
    if not csrf_token:
        form = await req.form()
        csrf_token = form.get("csrf_token")
        if not csrf_token:
            HTTPException(status_code=401, detail="CSRF not found")
    return csrf_token



async def csrf_validate(request: Request, store: StoreDep, csrf_token = Depends(get_csrf_token)) -> bool:
    exp = HTTPException(status_code=401, detail="CSRF validation error")
    if csrf_token:
        if key := request.cookies.get("session"):
            user_session: UserSession = await store.redis.get_session(key)
            if user_session:
                log.info(user_session.csrf_token)
                if csrf_token == str(user_session.csrf_token):
                    return True
    raise exp




async def validate_author_answer(request: Request, store: StoreDep, user_session: UserSession = Depends(get_current_user)) :
    user_id = user_session.id
    try:
        body: dict = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid JSON body",
        )

    question_id = body.get("question_id")
    if question_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="question_id is required",
        )

    try:
        question_id = int(question_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="question_id must be an integer",
        )
    
    question = await store.quesion.get_question_by_id(question_id)
    if not(question and question.author_id == user_id):
         raise HTTPException(status_code=403, detail="You are not author")

