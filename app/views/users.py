from pathlib import Path
import aiofiles
from fastapi import UploadFile
from app.core.config import config
from app.repository.redis import sessions
from app.schemas.user import User, UserUpdate
from app.views.base import BaseView
from app.repository.db import user as crud

class UserView(BaseView):

    async def _upload_avatar(self, file: UploadFile, user_id: int):
        upload_dir = Path("static/avatars")
        upload_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(file.filename).suffix or ".bin"
        filename = f"{user_id}{ext}"
        dest = upload_dir / filename

        async with aiofiles.open(dest, "wb") as f:
            content = await file.read()
            await f.write(content)
        return f"http://{config.server.host}:{config.server.port}/static/avatars/{filename}"

    async def profile_edit_get(self, user_id):
        user = await crud.get_user_by_id(self.session, user_id)
        return await self.template_response(
            "user.html", 
            {
                "user": user
            }
        )

    async def profile_edit_post(self, email: str, nickname: str, avatar: UploadFile, user_id: int):
        img_url = await self._upload_avatar(avatar, user_id) if avatar and avatar.filename else None
        user = await crud.update_user(
            self.session, 
            user_id, 
            UserUpdate(
                email=email,
                nickname=nickname,
                img_url=img_url
            )
        )
        key = self.request.cookies.get("session")
        if key is not None:
            await sessions.create_session(key, User(
                id=user.id,
                nickname=user.profile.nickname,
                email=user.email,
                img_url=user.profile.img_url
            ))
      
        return await self.template_response("user.html", {
            "user": user
            }
        )

