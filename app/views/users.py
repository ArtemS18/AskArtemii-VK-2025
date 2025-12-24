from logging import getLogger
from fastapi import UploadFile
from app.lib import fiels_utils
from app.schemas.error import ErrorTemplate
from app.schemas.user import UserSession, UserUpdate
from app.views.base import BaseView
import uuid

log = getLogger(__name__)


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
        
        try:
            await fiels_utils.validata_file(avatar)
        except fiels_utils.MaxFileSizeError:
            return await self.profile_edit_get(user_id, ErrorTemplate("Первышен допустимый размер файла (5 МБ)"))
        except fiels_utils.UnexeptSizeError:
            return await self.profile_edit_get(user_id, ErrorTemplate("Не указан размера файла"))
        except fiels_utils.EmptyFileError:
            avatar = None
        except fiels_utils.NotValidPostfix:
            return await self.profile_edit_get(user_id, ErrorTemplate("Разрешны файлы только с расширениями PNG/JPG"))
        log.info(avatar)
           
        img_url = None
        if avatar:
            img_url = await self.store.fiels.save_avatar(avatar, user_id)
            log.info(img_url)

        updated = {}
        for k, v in {"email": email, "nickname": nickname, "img_url": img_url}.items():
            if v is None or v == "":
                pass
            else:
                updated.update({k: v})
        
        user = await self.store.user.update_user(
            user_id, 
            UserUpdate(
                **updated,
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

