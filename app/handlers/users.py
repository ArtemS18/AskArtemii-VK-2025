from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.handlers.deps import UserViewDep
from app.core.config import config

api = config.endpoint
router = APIRouter(prefix=api.user)

@router.get("/me", response_class=HTMLResponse)
async def user_settings_view(view: UserViewDep):
    template = await view.user_settings()
    return template
