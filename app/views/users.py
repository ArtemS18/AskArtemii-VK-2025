from fastapi import UploadFile
from app.repository.minio.avatars import FileSizeError
from app.schemas.error import ErrorTemplate
from app.schemas.user import UserSession, UserUpdate
from app.views.base import BaseView
import uuid

class UserView(BaseView):

    async def profile_edit_get(self, user_id, error: ErrorTemplate | None = None):
        user = await self.store.user.get_user_by_id(user_id)
        return await self.template_response(
            "user.html", 
            {
                "error": error,
                "user": user
            }
        )

    async def profile_edit_post(self, email: str, nickname: str, avatar: UploadFile, user_id: int):
        img_url = None
        try:
            if avatar and avatar.file:
                img_url = await self.store.fiels.save_avatar(avatar, user_id)
        except FileSizeError:
            return await self.profile_edit_get(user_id, ErrorTemplate("Слишком большой файл!"))
        
        user = await self.store.user.update_user(
            user_id, 
            UserUpdate(
                email=email,
                nickname=nickname,
                img_url=img_url
            )
        )
        key = self.request.cookies.get("session")
        if key is not None:
            await self.store.redis.update_session(key, UserSession(
                id=user.id,
                nickname=user.profile.nickname,
                email=user.email,
                img_url=user.profile.img_url,
                csrf_token=uuid.uuid4()
            ))
      
        return await self.template_response("user.html", {
            "user": user
            }
        )

