from anyio import to_thread
from pathlib import Path
import aiofiles
from fastapi import Request, UploadFile
from app.core.config import config
from app.repository.redis import sessions
from app.schemas.user import User, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.views.base import BaseView
from app.repository.db import user as crud
from app.repository.minio.avatars import UserAvatarRepository

MAX_FILE_SIZE = 1024*1024*1024

class UserView(BaseView):
    def __init__(self,session: AsyncSession, request: Request,  user_avatars: UserAvatarRepository):
        super().__init__(session, request)
        self.user_avatars = user_avatars

    async def _upload_avatar_in_file(self, file: UploadFile, user_id: int):
        upload_dir = Path("static/avatars")
        upload_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(file.filename).suffix or ".bin"
        filename = f"{user_id}{ext}"
        dest = upload_dir / filename

        async with aiofiles.open(dest, "wb") as f:
            content = await file.read()
            await f.write(content)
        return f"http://{config.server.host}:{config.server.port}/static/avatars/{filename}"
    
    async def _get_size_of_uploadfile(self, file: UploadFile) -> int:
        await file.seek(0, 2)
        size = to_thread.run_sync(file.file.tell)
        await file.seek(0) 
        return size
    
    async def _upload_avatar(self, file: UploadFile, user_id: int):
        await self.user_avatars.create_bucket()

        ext = Path(file.filename).suffix or ".bin"
        url = await self.user_avatars.save_avatar_with_url(file.file, user_id, ext)

        return url

    async def profile_edit_get(self, user_id):
        user = await crud.get_user_by_id(self.session, user_id)
        return await self.template_response(
            "user.html", 
            {
                "user": user
            }
        )

    async def profile_edit_post(self, email: str, nickname: str, avatar: UploadFile, user_id: int):
        if self._get_size_of_uploadfile(avatar) > MAX_FILE_SIZE:
            return await self.profile_edit_get(user_id)
        
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

