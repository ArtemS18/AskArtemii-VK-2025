import time
import jwt
from fastapi import APIRouter, Depends

from app.schemas.user import UserSession
from .deps import get_existed_user
from app.core.config import config

router = APIRouter()

@router.get("/centrifugo/token")
async def centrifugo_token(user: UserSession=Depends(get_existed_user)):
    user_id = str(user.id) if user else "anon"

    payload = {
        "sub": user_id,
        "exp": int(time.time()) + 60 * 99,
    }
    token = jwt.encode(payload, config.centrifugo_jwt_key, algorithm="HS256")
    return {"token": token}
