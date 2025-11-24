from app.views.base import BaseView


class UserView(BaseView):
    async def user_settings(self):
        template = await self.template_response("user.html")
        return template
