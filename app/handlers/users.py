from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from app.handlers.deps import UserViewDep, get_current_user
from app.core.config import config
from app.models.users import UserORM, UserProfileORM
from pathlib import Path
from pydantic import BaseModel
import aiofiles

from app.schemas.user import User

api = config.endpoint
router = APIRouter(prefix=api.user)

class UserEditForm(BaseModel):
    email: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None

@router.get("/edit", response_class=HTMLResponse)
async def user_settings_view(view: UserViewDep, user: User = Depends(get_current_user)):
    template = await view.profile_edit_get(user.id)
    return template

@router.post("/edit")
async def user_settings_post(
    view: UserViewDep,
    email: str = Form(None),
    nickname: str = Form(None),
    avatar: UploadFile | None = None,
    user: User = Depends(get_current_user),
):
    
    return await view.profile_edit_post(email, nickname, avatar,  user.id)